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
        self._x: List[NDArray[np.int64]] = []
        # probs of output, (B, 1)
        self._logp: NDArray[np.float64] = 0
        self.bos = bos
        self.eos = eos
        self.max_len = max_len
        self._length = 0
        self._bw_len = 0
        self.p_arg1 = np.log(self.max_len)

    @property
    def bw_len(self):
        return self._bw_len

    @bw_len.setter
    def bw_len(self, l: int):
        self._bw_len = l

    @property
    def x(self):
        return np.concatenate(self._x, axis=1)

    @x.setter
    def x(self, _x):
        self._x = _x
        self._length = len(_x)

    @property
    def length(self):
        return self._length

    @property
    def log_prob(self):
        return self._logp

    @log_prob.setter
    def log_prob(self, _logp: NDArray[np.float64]):
        self._logp = _logp

    def is_done(self):
        d = (self._x[-1] == self.eos).all() or self._length > self.max_len
        return d

    def penalize(self, x: int):
        # ln(3) ~= 1.09
        # if x < 3:
        #     return -1e6
        # y = (np.log(x) - 1.09) / (self.p_arg1 - 1.09)
        # if self._length < self._bw_len:
        #     return -10
        return 0

    @property
    def score(self):
        # TODO: add more score methods
        # penal = self.penalize(self._length)
        # mean < 0, median < 0
        # score = (np.mean(self.log_prob) + np.median(self.log_prob)) / 2
        score = np.mean(self.log_prob)
        return score

    @property
    def pred_ids(self):
        return np.concatenate(self._x, axis=1)


class NodeManagerBase(object):
    def __init__(self, max_node: int, batch_node: int = 1) -> None:
        assert batch_node <= max_node, f"one batch must less than max node"
        self.max_node = max_node
        self.batch_node = batch_node
        self.node_list: List[BeamSearchNode] = []
        self.rng = np.random.default_rng()

    def __len__(self):
        return len(self.node_list)

    def push(self, node: BeamSearchNode):
        if len(self.node_list) + 1 > self.max_node:
            idx = self.get_worst_node_idx()
            worst_node = self.node_list[idx]
            if node.score < worst_node.score:
                return
            del self.node_list[idx]
        self.node_list.append(node)

    def push_n(self, nodes: List[BeamSearchNode]):
        new_nodes = sorted(
            [*self.node_list, *nodes],
            key=lambda node: node.score,
            reverse=True,
        )
        self.node_list = new_nodes[: self.max_node]

    def is_empty(self):
        return len(self) == 0

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
    def get(self):
        l = len(self)
        if l == 0:
            return None
        # self.align_len()
        if self.batch_node <= l:
            idxs = self.rng.choice(np.arange(l), size=self.batch_node, replace=False)
        else:
            idxs = np.arange(l)
        nodes = [self.node_list[i] for i in idxs]
        self.node_list = np.delete(self.node_list, idxs).tolist()
        return nodes

    def align_len(self):
        node_len = np.asarray([n.x.shape[1] for n in self.node_list], dtype=np.int16)
        idxs = ~(node_len == np.bincount(node_len).argmax())
        self.node_list = np.delete(self.node_list, idxs).tolist()

    def delete(self, node: BeamSearchNode):
        for i, n in enumerate(self.node_list):
            if n == node:
                del self.node_list[i]
                return n


class DoneNodeManager(NodeManagerBase):
    def sort_(self):
        self.node_list = sorted(self.node_list, key=lambda n: n.score, reverse=True)

    @property
    def all_nodes(self):
        self.sort_()
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
        self._max_done_counter = beam_width
        self.active_nodes = ActiveNodeManager(
            max_node=beam_width**2,
            batch_node=beam_width**2,
        )
        self.done_nodes = DoneNodeManager(max_node=beam_width)

    def search(self, start_tokens: np.ndarray):
        """
        params:
            start_tokens: B * 1
        return:
            out: B * beam_width * N
        """
        self.init_state(start_tokens=start_tokens)
        # for _ in range(10):
        #     self.step()
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

    def stack_bw(self, nodes: List[BeamSearchNode]) -> List[np.ndarray]:
        lens = np.unique([n.length for n in nodes])
        node_p = [[n for n in nodes if n.length == l] for l in lens]
        x_in = [np.concatenate([n.x for n in nn], axis=0) for nn in node_p]
        return x_in

    def step_one(self, nodes: List[BeamSearchNode]) -> List[BeamSearchNode]:
        # nodes: [BW_B]
        bwb = len(nodes)
        node_p = self.stack_bw(nodes)
        # [BW_B, (B, vocab_size)]
        # logits_flat = []
        log_prob_flat = []
        top_ids_flat = []
        for x_ins in node_p:
            nn: int = x_ins.shape[0]
            _memory = [np.concatenate([self._memory[0]] * nn, axis=0)]
            logits_stack = self._decoder(x_ins, _memory)
            prob = np.log(self.softmax(logits_stack, axis=1))
            ids = np.argsort(logits_stack, axis=1)[:, ::-1]
            n: int = logits_stack.shape[0]
            b: int = n // nn
            # logits_flat_tmp = [logits_stack[i : i + b] for i in range(0, n, b)]
            prob_tmp = [prob[i:i+b] for i in range(0, n, b)]
            ids_tmp = [ids[i:i+b] for i in range(0, n, b)]
            # logits_flat.extend(logits_flat_tmp)
            log_prob_flat.extend(prob_tmp)
            top_ids_flat.extend(ids_tmp)
        # logits_flat = [self._decoder(node.x, self._memory) for node in nodes]
        # BW_B*BW
        out = []
        for i in range(bwb):
            # (B, vocab_size)
            # log_prob = np.log(self.softmax(logits, axis=1))
            log_prob = log_prob_flat[i]
            # (B, vocab_size)
            # top_ids = np.argsort(logits, axis=1)[:, ::-1]
            top_ids = top_ids_flat[i]
            # length: beam_width
            for j in range(self._beam_width):
                top_id = top_ids[:, j]  # (B, 1)
                node = BeamSearchNode(
                    bos=self._bos,
                    eos=self._eos,
                    max_len=self._max_iter,
                )
                # node.x = np.concatenate([nodes[i].x, top_id[..., np.newaxis]], axis=1)
                node.x = [*nodes[i]._x, top_id[..., np.newaxis]]
                # (B, 1)
                node.log_prob = nodes[i].log_prob + log_prob[:, top_id]
                out.append(node)
        return out
    def step(self):
        in_nodes = self.active_nodes.get()
        out_nodes = self.step_one(in_nodes)
        done_nodes = [n for n in out_nodes if n.is_done()]
        act_nodes = [n for n in out_nodes if not n.is_done()]
        self.crt_done_counter += len(done_nodes)
        if len(done_nodes) > 0:
            self.done_nodes.push_n(done_nodes)
        self.active_nodes.push_n(act_nodes)

    def init_state(self, start_tokens: np.ndarray):
        # start_tokens: (B, 1)
        node = BeamSearchNode(self._bos, self._eos, self._max_iter)
        node.x = [start_tokens]
        node.log_prob = np.zeros((start_tokens.shape[0], 1))
        self.active_nodes.push(node)


if __name__ == "__main__":
    ...
