import re
from typing import List, Optional, Tuple, Union
import numpy as np
import onnxruntime
from PIL import Image
from tokenizers import Tokenizer
from tokenizers.models import BPE

from ..utils.config import Config
from ..utils.transforms import get_transforms
from ..utils.beam_search import CeleryBeamSearch


class LatexModelONNX(object):
    __supported_methods__ = ("greedy", "beam")
    transforms = None

    def __init__(
        self,
        encoder: str,
        decoder: str,
        min_img_size=(32, 32),
        max_img_size=(192, 896),
        max_seq_len: int = 512,
        bos_token: int = 1,
        eos_token: int = 2,
        pad_token: int = 0,
        tokenizer_path: str = None,
        filter_thres: float = 0.9,
        temperature: float = 0.5,
        search_method="greedy",
    ):
        super(LatexModelONNX, self).__init__()
        self.encoder = onnxruntime.InferenceSession(encoder)
        self.decoder = onnxruntime.InferenceSession(decoder)

        self.max_seq_len = max_seq_len
        self.bos_token = bos_token
        self.eos_token = eos_token
        self.pad_token = pad_token
        self.filter_thres = filter_thres
        self.temperature = temperature
        self.search_method = search_method

        self.transforms = get_transforms(min_img_size, max_img_size)
        assert tokenizer_path is not None, "Tokenizer path must be provided"
        self.tokenizer: Tokenizer = None
        self.load_tokenizer(tokenizer_path)

    def load_tokenizer(self, tokenizer_path: str):
        tokenizer = Tokenizer(BPE())
        self.tokenizer = tokenizer.from_file(tokenizer_path)

    def token2str(self, tokens: Union[np.ndarray, List]) -> List[str]:
        dec = [self.tokenizer.decode_batch([tbw[0] for tbw in tb]) for tb in tokens]
        dec = [
            [
                "".join(d.split(" "))
                .replace("Ġ", " ")  # space
                .replace("Ċ", "")  # newline
                .replace("[EOS]", "")
                .replace("[BOS]", "")
                .replace("[PAD]", "")
                .strip()
                for d in dbw
            ]
            for dbw in dec
        ]
        # (B, BW)
        return dec

    def detokenize(self, tokens: Union[np.ndarray, List]):
        # TODO: complete the decode to return list
        # tokens: (B, BW, (N, float))
        toks: List[List[List[str]]] = [
            [[self.tokenizer.id_to_token(t) for t in tb] for tb in tbw]
            for tbw in tokens
        ]
        for bw in range(len(toks)):
            for b in range(len(bw)):
                for i in reversed(range(len(toks[b]))):
                    if toks[b][i] is None:
                        toks[b][i] = ""
                    toks[b][i] = toks[b][i].replace("Ġ", " ").replace("Ċ", "").strip()
                    if toks[b][i] in ("[BOS]", "[EOS]", "[PAD]"):
                        del toks[b][i]
        return toks

    def post_process(self, s: str) -> str:
        """
        modified from https://github.com/lukas-blecher/LaTeX-OCR, thanks!
        Remove unnecessary whitespace from LaTeX code.
        Args:
            s (str): Input string
        Returns:
            str: Processed latex string
        """
        text_reg = r"(\\(operatorname|mathrm|text|mathbf)\s?\*? {.*?})"
        letter = "[a-zA-Z]"
        noletter = "[\W_^\d]"
        names = [x[0].replace(" ", "") for x in re.findall(text_reg, s)]
        s = re.sub(text_reg, lambda match: str(names.pop(0)), s)
        news = s
        while True:
            s = news
            news = re.sub(r"(?!\\ )(%s)\s+?(%s)" % (noletter, noletter), r"\1\2", s)
            news = re.sub(r"(?!\\ )(%s)\s+?(%s)" % (noletter, letter), r"\1\2", news)
            news = re.sub(r"(%s)\s+?(%s)" % (letter, noletter), r"\1\2", news)
            if news == s:
                break
        return s

    def preprocess(self, imgs: List[Union[Image.Image, np.ndarray]]):
        if not isinstance(imgs, list):
            imgs = [imgs]
        # imgs: B C H W
        imgs: np.ndarray = np.concatenate(
            [self.transforms(img) for img in imgs], axis=0
        )
        assert len(imgs.shape) == 3, "Image must be at least 3D"
        return np.expand_dims(imgs, 1)  # B C H W

    def greedy(self):
        self.search_method = "greedy"

    def beam(self):
        self.search_method = "beam"

    def softmax(self, x: np.ndarray, dim=-1):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=dim, keepdims=True)  # B*T

    def beam_search(
        self,
        start_tokens: np.ndarray,
        memory: List[np.ndarray],
        temperature: float = 0.2,
    ):
        beam_width = 10
        beam_searcher = CeleryBeamSearch(
            memory=memory,
            decode_fn=self.decoder_run,
            beam_width=beam_width,
            bos=self.bos_token,
            eos=self.eos_token,
            max_iter=self.max_seq_len,
        )
        preds = beam_searcher.search(start_tokens=start_tokens)
        return preds

    def decoder_run(self, x: np.ndarray, memory: List[np.ndarray]):
        tgt_mask = np.triu(np.full((x.shape[1]), -np.inf), k=1).astype(bool)
        dec_inputs = {
            self.decoder.get_inputs()[0].name: x.astype(np.int64),  # B * T
            self.decoder.get_inputs()[1].name: memory[0],  # B * HW * D
            self.decoder.get_inputs()[2].name: tgt_mask,  # T * T
        }
        logits: np.ndarray = self.decoder.run(None, dec_inputs)[0][
            :, -1, :
        ]  # B * vocab_size
        return logits

    def greedy_search(
        self,
        start_tokens: np.ndarray,
        memory: List[np.ndarray],
        temperature: float = 0.2,
    ):
        out = start_tokens.astype(np.int64)  # B * N
        prob = None
        for _ in range(self.max_seq_len):
            x = out[:, -self.max_seq_len :]
            logits = self.decoder_run(x, memory=memory)
            # TODO: finish sample generate
            # TODO: add more sampling method
            # k = int((1 - self.filter_thres) * logits.shape[-1])
            # idx: np.ndarray = np.argpartition(logits, -k, axis=1)[:, :-k]
            # for i in range(idx.shape[0]):
            #     logits[i, idx[i]] = -np.inf
            # probs: np.ndarray = self.softmax(logits/temperature, dim=1)
            # sample = [np.random.choice(np.arange(probs.shape[1]), 1, p=pp) for pp in probs]
            # sample = np.array(sample, dtype=int)
            # argmax prob sample
            probs: np.ndarray = self.softmax(logits / temperature, dim=1)
            sample = probs.argmax(axis=1)[..., np.newaxis]
            prob = [probs[b][sample[b]] for b in range(sample.shape[0])]
            # if generate all pad_token, stop
            end_pad = (sample == self.pad_token).all()
            if end_pad:
                sample = np.ones_like(sample) * self.eos_token
            out: np.ndarray = np.concatenate((out, sample), axis=1)
            end_eos = (np.cumsum(out == self.eos_token, 1)[:, -1] >= 1).all()
            if end_eos:
                break
        return [[[out[b], prob[b][0]]] for b in range(out.shape[0])]

    def generate(
        self,
        start_tokens: np.ndarray,
        memory: List[np.ndarray],
        temperature: float = 0.2,
    ):
        if self.search_method == "greedy":
            return self.greedy_search(
                start_tokens=start_tokens,
                memory=memory,
                temperature=temperature,
            )
        elif self.search_method == "beam":
            return self.beam_search(
                start_tokens=start_tokens,
                memory=memory,
                temperature=temperature,
            )
        else:
            raise ValueError(f"search method {self.search_method} not supported")

    def forward(self, src: np.ndarray, temperature: float = 0.2) -> List[str]:
        enc_inputs = {
            self.encoder.get_inputs()[0].name: src,
        }
        memory: List[np.ndarray] = self.encoder.run(None, enc_inputs)
        # B * 1
        start_tokens = np.ones((src.shape[0], 1), dtype=int) * self.bos_token
        # B * BW * N
        output = self.generate(
            start_tokens=start_tokens,
            memory=memory,
            temperature=temperature,
        )
        return output

    # def save_img(self, img: np.ndarray, name="test.png"):
    #     import matplotlib.pyplot as plt
    #     plt.imsave(name, img[0], cmap="gray")

    def __call__(
        self,
        src: List[Union[Image.Image, np.ndarray]],
        temperature: float = 0.2,
        method: str = None,
        out_list=False,
    ) -> List[str]:
        if method is not None:
            assert (
                method in self.__supported_methods__
            ), f"method {method} not supported"
            self.search_method = method
        src: np.ndarray = self.preprocess(src)  # B C H W
        # (List[(B, N)])
        preds = self.forward(src, temperature)
        if preds is None:
            return None
        b, bw = len(preds), len(preds[0])
        if out_list:
            outstr = self.detokenize(preds)
        else:
            outstr = self.token2str(preds)
        # (B, BW, (str, float))
        output = [[[outstr[i][j], preds[i][j][1]] for j in range(bw)] for i in range(b)]
        return output


def get_model(conf: Config) -> LatexModelONNX:
    model = LatexModelONNX(
        encoder=conf.encoder_path,
        decoder=conf.decoder_path,
        max_seq_len=conf.max_seq,
        min_img_size=conf.min_img_size,
        max_img_size=conf.max_img_size,
        bos_token=conf.bos_token,
        eos_token=conf.eos_token,
        pad_token=conf.pad_token,
        temperature=conf.temperature,
        tokenizer_path=conf.tokenizer_path,
        search_method=conf.search_method,
    )
    return model


if __name__ == "__main__":
    ...
