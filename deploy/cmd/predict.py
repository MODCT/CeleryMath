# from pathlib import Path
import numpy as np
# from viztracer import VizTracer
from argparse import ArgumentParser
from PIL import Image

from ..models.model import LatexModelONNX, get_model
from ..utils.config import Config
from ..utils.utils import post_process, timer, seed_everything

@timer
def main(impath: str, conf: Config):
    model: LatexModelONNX = get_model(conf)

    img = Image.open(impath, ).convert("L")  # H W
    # img = np.array(img, dtype=np.float32)[np.newaxis, ...]
    # transforms = get_transforms(conf.min_img_size, conf.max_img_size)
    # img = transforms(img)
    # with VizTracer(output_file="./predict.html") as viztracer:
    #     res = model([img])
    res = model([img, ])
    print(post_process(res[0]))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", dest="image", type=str, help="image to predict")
    parser.add_argument("-c", dest="config", type=str, help=".json config file")
    args = parser.parse_args([
        "-i", "tmp/test-3.png",
        "-c", "deploy/conf/conf.json",
    ])
    seed_everything(241)
    main(args.image, Config(args.config))
