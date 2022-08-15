"""
Description: Beam Search
Author: Rainyl
Date: 2022-08-15 15:36:13
LastEditTime: 2022-08-15 15:36:14
"""
from enum import Enum
from typing import Callable, Dict, List
import numpy as np


class CeleryBeamSearch(object):
    crt_iter = 0
    active_seq: np.ndarray = None  # B * beam_width * N
    active_probs: np.ndarray = None  # B * beam_width
    seq_finished: np.ndarray = None  # B * beam_width

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
        return self.active_seq

    def is_finished(self):
        if self.crt_iter > self._max_iter:
            return True
        self.crt_iter += 1
        self.seq_finished = np.array(
            [
                [
                    (self.active_seq[i][j] == self._eos).astype(int).sum() > 0
                    for j in range(self._beam_width)
                ]
                for i in range(self.active_seq.shape[0])
            ]
        )
        if self.seq_finished.all():
            return True
        return False

    def softmax(self, x: np.ndarray, dim=-1) -> np.ndarray:
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=dim, keepdims=True)  # B*T

    def step(self):
        new_beam_score = []  # BW * B * BW
        new_beam_seq = []  # BW * B * BW
        for i in range(self._beam_width):
            x = self.active_seq[:, i, :]  # prev beam i
            logits = self._decoder(x, self._memory)
            topk = np.argsort(logits, axis=1)[:, ::-1][:, : self._beam_width]
            new_beam_seq.append(topk)
            probs = self.softmax(logits, dim=1)
            probs_topk = np.array(
                [logits[j][topk[j]] for j in range(probs.shape[0])],
                dtype=np.float32,
            )
            prev_prob = np.tile(
                self.active_probs[:, i][..., np.newaxis], [1, self._beam_width]
            )
            new_beam_score.append(probs_topk + prev_prob)
        # B*BW**2*N
        seqs = np.array(
            [
                [
                    [*self.active_seq[j, i, :], new_beam_seq[i][j][k]]
                    for i in range(self._beam_width)
                    for k in range(self._beam_width)
                ]
                for j in range(self.active_seq.shape[0])
            ],
            dtype=np.int32,
        )
        # B*BW**2
        scores = np.vstack(
            [
                new_beam_score[i][:, j]
                for i in range(self._beam_width)
                for j in range(self._beam_width)
            ]
        ).T
        idxs = np.argsort(scores, axis=1)[:, ::-1][:, : self._beam_width]
        self.active_seq = np.asarray([seqs[i][idxs[i]] for i in range(idxs.shape[0])])
        self.active_probs = np.asarray(
            [scores[i][idxs[i]] for i in range(idxs.shape[0])]
        )
        # print("debug")

    def init_state(self, start_tokens: np.ndarray):
        # init active seq shape: B * beam_width * 1
        logits = self._decoder(start_tokens, self._memory)  # B*vocab_size
        # B*beam_width
        topk = np.argsort(logits, axis=1)[:, ::-1][:, : self._beam_width]
        self.active_seq = np.tile(
            np.expand_dims(start_tokens, axis=1),
            [1, self._beam_width, 1],
        ).astype(np.int32)
        self.active_seq = np.concatenate(
            (self.active_seq, np.expand_dims(topk, 2)),
            axis=2,
            dtype=np.int32,
        )
        probs = self.softmax(logits, dim=1)
        self.active_probs = np.array(
            [logits[i][topk[i]] for i in range(probs.shape[0])],
            dtype=np.float32,
        )
        # self.active_probs = np.tile(
        #     np.array(
        #         [[0.0] + [-np.inf] * (self._beam_width - 1)],
        #         dtype=np.float32,
        #     ),
        #     [start_tokens.shape[0], 1],
        # )

        # self.finished_seq = np.zeros_like(self.active_seq, dtype=np.int32)
        # self.finished_score = np.zeros_like(self.active_log_probs, dtype=np.float32)
        # self.finished_flags = np.zeros_like(self.active_log_probs, dtype=np.bool8)


def seed_everything(seed: int):
    """
    from https://gist.github.com/ihoromi4/b681a9088f348942b01711f251e5f964
    thanks!
    """
    import random, os
    import numpy as np

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


if __name__ == "__main__":
    seed_everything(241)
    mem = np.random.normal(size=(2, 168, 512))

    def fun(x, memory):
        return np.random.normal(size=(2, 8000))

    searcher = CeleryBeamSearch(
        memory=mem,
        decode_fn=fun,
    )
    searcher.search(np.ones((2, 1)))
