import json
from typing import Dict, Sequence, Union


class Config(object):
    encoder_path = ""
    decoder_path = ""
    tokenizer_path = ""
    device = "cpu",
    pad_token = 0,
    bos_token = 1,
    eos_token = 2,
    temperature = 0.2
    max_seq = 512
    min_img_size = [32, 32]
    max_img_size = [192, 896]

    def __init__(self, conf_path: str):
        self.load(conf_path)

    def load(self, conf_path: str):
        with open(conf_path, 'r', encoding="utf-8") as f:
            conf: Dict[str, Union[str, int]] = json.load(f)
        for k, v in conf.items():
            setattr(self, k, v)


if __name__ == "__main__":
    ...