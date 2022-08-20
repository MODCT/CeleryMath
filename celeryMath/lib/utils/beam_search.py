"""
Description: Beam Search
Author: Rainyl
Date: 2022-08-15 15:36:13
LastEditTime: 2022-08-15 15:36:14
"""
from typing import Callable, Dict, List, Optional, Union
from numpy.typing import NDArray
import numpy as np


class BeamSearchNode(object):
    def __init__(self, bos=1, eos=2, max_len=512):
        # input to fn, (B, T)
        self._x: NDArray[np.int64] = None
        # output of fn, (B, 1)
        self._ids: NDArray[np.int64] = None
        # probs of output, (B, 1)
        self._logp: NDArray[np.float64] = None
        self.bos = bos
        self.eos = eos
        self.max_len = max_len
        self._length = 0
        self.p_arg1 = np.log(self.max_len)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, _x):
        self._x = _x
        self._length = self._x.shape[1] + 1

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, _ids):
        idx = self._x[:, -1] == self.eos
        if idx.any():
            _ids[idx] = self.eos
        self._ids = _ids

    @property
    def log_prob(self):
        return self._logp

    @log_prob.setter
    def log_prob(self, _logp: NDArray[np.float64]):
        self._logp = _logp

    def is_done(self):
        d = (self._x[:, -1] == self.eos).all() or self._length > self.max_len
        return d

    def penalize(self, x: int):
        # ln(3) ~= 1.09
        if x < 3:
            return -1e6
        y = (np.log(x) - 1.09) / (self.p_arg1 - 1.09)
        return np.log(y)

    @property
    def score(self):
        # TODO: add more score methods
        # (mean + median) * penalize
        # penalize: [0, 1]
        # penal = self.penalize(self._length)
        # mean < 0, median < 0
        score = (np.mean(self.log_prob) + np.median(self.log_prob)) / 2
        return score

    @property
    def pred_ids(self):
        return self._x


class NodeManagerBase(object):
    def __init__(self, max_node: int) -> None:
        self.max_node = max_node
        self.node_list: List[BeamSearchNode] = []

    def __len__(self):
        return len(self.node_list)

    def push(self, node: BeamSearchNode):
        if len(self.node_list) + 1 >= self.max_node:
            idx = self.get_worst_node_idx()
            worst_node = self.node_list[idx]
            if node.score < worst_node.score:
                return
            self.del_worst_node()
        self.node_list.append(node)

    def is_empty(self):
        return len(self.node_list) == 0

    def get_worst_node_idx(self):
        score = 1e6
        idx = -1
        for i, n in enumerate(self.node_list):
            if n.score < score:
                score = n.score
                idx = i
        return idx

    def del_worst_node(self):
        idx = self.get_worst_node_idx()
        if idx == -1:
            return
        del self.node_list[idx]


class ActiveNodeManager(NodeManagerBase):
    def get_one(self):
        if len(self.node_list) == 0:
            return None
        idx = np.random.randint(0, len(self.node_list))
        n = self.node_list[idx]
        del self.node_list[idx]
        return n

    def push(self, node: BeamSearchNode):
        if len(self.node_list) + 1 >= self.max_node:
            idx = self.get_worst_node_idx()
            worst_node = self.node_list[idx]
            if node.score < worst_node.score:
                return
            self.del_worst_node()
        self.node_list.append(node)

    def delete(self, node: BeamSearchNode):
        for i, n in enumerate(self.node_list):
            if n == node:
                del self.node_list[i]
                return n


class DoneNodeManager(NodeManagerBase):
    def push(self, node: BeamSearchNode):
        if len(self.node_list) + 1 > self.max_node:
            idx = self.get_worst_node_idx()
            worst_node = self.node_list[idx]
            if node.score < worst_node.score:
                return
            self.del_worst_node()
        self.node_list.append(node)

    def sort(self):
        scores = [n.score for n in self.node_list]
        idx = np.argsort(scores)[::-1]
        self.node_list = [self.node_list[i] for i in idx]

    @property
    def all_nodes(self):
        self.sort()
        return self.node_list


class CeleryBeamSearch(object):
    crt_iter = 0
    crt_done_counter = 0

    def __init__(
        self,
        memory: np.ndarray,
        decode_fn: Callable[[np.ndarray, List[np.ndarray]], (np.ndarray)],
        beam_width=5,
        bos=1,
        eos=2,
        max_iter=512,
    ):
        self._memory = memory
        self._decoder = decode_fn
        self._beam_width = beam_width
        self._bos = bos
        self._eos = eos
        self._max_iter = max_iter
        self._max_done_counter = beam_width * 2
        self.active_nodes = ActiveNodeManager(max_node=self._beam_width*2)
        self.done_nodes = DoneNodeManager(max_node=beam_width)

    def search(self, start_tokens: np.ndarray):
        """
        params:
            start_tokens: B * 1
        return:
            out: B * beam_width * N
        """
        self.init_state(start_tokens=start_tokens)
        while not self.is_finished():
            self.step()
        preds = self.gather_done()
        return preds

    def is_finished(self):
        """
        TODO: improve this:
        For now, the stop of search mainly rely on
        current done counter due to the huge calculation
        of active_nodes, the self.active_nodes.is_empty()
        is not easy to satisfy.
        """
        if self.crt_done_counter > self._max_done_counter:
            return True
        if self.crt_iter > self._max_iter:
            return True
        # self.crt_iter += 1
        if self.active_nodes.is_empty() and not self.done_nodes.is_empty():
            return True
        return False

    def softmax(self, x: np.ndarray, axis=-1) -> np.ndarray:
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=axis, keepdims=True)  # B*T

    def gather_done(self):
        nodes = self.done_nodes.all_nodes
        if len(nodes) == 0:
            return None
        batch_size = nodes[0].x.shape[0]
        # (B, BW)
        probs = self.softmax(
            np.asarray(
                [[node.log_prob[i, 0] for node in nodes] for i in range(batch_size)]
            ),
            axis=1,
        )
        # (B, BW, 2(N, float))
        samples = [
            [[node.pred_ids[i], probs[i, j]] for j, node in enumerate(nodes)]
            for i in range(batch_size)
        ]
        return samples

    # TODO: sample methods
    def nuc_sample(self, probs: NDArray[np.float32], p: float = 0.9):
        ...

    def step_one(self, x_in: BeamSearchNode) -> List[BeamSearchNode]:
        # (B, vocab_size)
        logits = self._decoder(x_in.x, self._memory)
        # (B, vocab_size)
        log_prob = np.log(self.softmax(logits, axis=1))
        # (B, beam_width)
        top_ids = np.argsort(logits, axis=1)[:, ::-1]
        # length: beam_width
        out = []
        for i in range(self._beam_width):
            top_id = top_ids[:, i]  # (B, 1)
            node = BeamSearchNode(bos=self._bos, eos=self._eos, max_len=self._max_iter)
            node.x = np.vstack((x_in.x.T, top_id)).T
            node.ids = top_id
            # (B, 1)
            node.log_prob = x_in.log_prob + log_prob[:, top_id]
            out.append(node)
        return out

    def step(self):
        # TODO: parallel
        in_node = self.active_nodes.get_one()
        out_nodes = self.step_one(in_node)
        for node in out_nodes:
            if node.is_done():
                self.done_nodes.push(node)
                self.crt_done_counter += 1
            else:
                self.active_nodes.push(node)

    def init_state(self, start_tokens: np.ndarray):
        # start_tokens: (B, 1)
        node = BeamSearchNode(self._bos, self._eos, self._max_iter)
        node.x = start_tokens
        node.log_prob = np.zeros((start_tokens.shape[0], 1))
        self.active_nodes.push(node)


if __name__ == "__main__":
    ...
