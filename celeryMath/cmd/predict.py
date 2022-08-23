import sys
# from viztracer import VizTracer
from argparse import ArgumentParser
from PIL import Image

sys.path.append("..")
from lib.models.model import LatexModelONNX, get_model
from lib.utils.config import Config
from lib.utils.utils import post_process, timer, seed_everything

class Args:
    image: str
    config: Config

@timer
def main(impath: str, conf: Config):
    # model: LatexModelONNX = get_model(conf)

    img = Image.open(impath, ).convert("L")  # H W
    # img = np.array(img, dtype=np.float32)[np.newaxis, ...]
    # transforms = get_transforms(conf.min_img_size, conf.max_img_size)
    # img = transforms(img)
    # with VizTracer(output_file="./predict.html") as viztracer:
    #     res = model([img])
    res = model([img, ])
    print(res)
    # print(post_process(res[0]))


def timeit():
    main("tmp/a.png", Config("conf/conf.json"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", dest="image", type=str, help="image to predict")
    parser.add_argument("-c", dest="config", type=str, help=".json config file")
    args: Args = parser.parse_args([
        "-i", "tmp/a.png",
        "-c", "conf/conf.json",
    ])
    # args: Args = parser.parse_args()
    seed_everything(241)
    model: LatexModelONNX = get_model(Config(args.config))
    main(args.image, Config(args.config))
