import json
from typing import Dict, Sequence, Union
import os


class Config(object):
    encoder_path = ""
    decoder_path = ""
    tokenizer_path = ""
    device = "cpu"
    pad_token = 0
    bos_token = 1
    eos_token = 2
    temperature = 0.2
    beam_width = 3
    max_seq = 512
    min_img_size = (32, 32)
    max_img_size = (192, 896)
    snip_hotkey = "Ctrl+Alt+S"
    search_method = "greedy"
    sampling = "nucleus"

    def __init__(self, conf_path: str = "conf/conf.json"):
        self.conf_path = conf_path
        if os.path.exists(conf_path):
            self.load(conf_path)
        else:
            self.save(conf_path)

    def __str__(self) -> str:
        s = (
            f"Config(\n"
            f"\tencoder: {self.encoder_path},\n"
            f"\tdecoder: {self.decoder_path},\n"
            f"\tdevice: {self.device},\n"
            f"\ttokenizer: {self.tokenizer_path},\n"
            f"\ttemperature: {self.temperature},\n"
            f"\tsearch method: {self.search_method},\n"
            f"\tsampling: {self.sampling},\n"
            f"\tbeam_width: {self.beam_width},\n"
            f")"
        )
        return s

    def load(self, conf_path: str):
        with open(conf_path, "r", encoding="utf-8") as f:
            conf: Dict[str, Union[str, int]] = json.load(f)
        for k, v in conf.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @property
    def json(self):
        js = {
            "tokenizer_path": self.tokenizer_path,
            "encoder_path": self.encoder_path,
            "decoder_path": self.decoder_path,
            "device": self.device,
            "snip_hotkey": self.snip_hotkey,
            "search_method": self.search_method,
            "sampling": self.sampling,
            "temperature": self.temperature,
            "beam_width": self.beam_width,
        }
        return js

    def save(self, p: str | None = None):
        conf = {
            "tokenizer_path": self.tokenizer_path,
            "encoder_path": self.encoder_path,
            "decoder_path": self.decoder_path,
            "snip_hotkey": self.snip_hotkey,
            "search_method": self.search_method,
            "sampling": self.sampling,
            "temperature": self.temperature,
            "beam_width": self.beam_width,
            "device": self.device,
            "pad_token": self.pad_token,
            "bos_token": self.bos_token,
            "eos_token": self.eos_token,
            "max_seq": self.max_seq,
            "min_img_size": self.min_img_size,
            "max_img_size": self.max_img_size,
        }
        p = p or self.conf_path
        with open(p, "w") as f:
            json.dump(conf, f, indent=4)


if __name__ == "__main__":
    ...
