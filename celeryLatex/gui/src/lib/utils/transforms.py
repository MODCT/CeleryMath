from typing import Tuple, Union
import numpy as np
from PIL import Image


class DeployTransform(object):
    _buckets_ = [32, 64, 96, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896]

    def __init__(self, min_img_size, max_img_size, mean=0.7931, std=0.1738, interp=Image.BILINEAR):
        """
            process for every single image
        """
        self.pad_resize = PadMaxResize(min_img_size, max_img_size, interp)
        self.max_img_size = max_img_size
        self.mean = mean
        self.std = std
        self.buckets = [[i, j] for i in self._buckets_ for j in self._buckets_]

    def pad_image(self, img: np.ndarray):
        """
            TODO: make pad image more clever, ie. don't pad all image to the max shape
        """
        # img: C H W
        new_size = self.get_new_size(img.shape[1:])
        pw = new_size[-1] - img.shape[-1]
        ph = new_size[-2] - img.shape[-2]
        img = np.pad(img, ((0, 0), (0, ph), (0, pw)), "constant", constant_values=(0, ))
        return img

    def get_new_size(self, old_size: Tuple[int]):
        d1, d2 = old_size
        for (d1_b, d2_b) in self.buckets:
            if d1_b >= d1 and d2_b >= d2:
                return d1_b, d2_b
        # no match, return max (last one)
        return self.buckets[-1]

    def normalize(self, img: np.ndarray):
        img = (img - self.mean) / self.std
        return img

    # def save_img(self, img: np.ndarray, name="test.png"):
    #     import matplotlib.pyplot as plt
    #     plt.imsave(name, img, cmap="gray")

    def resize(self, img: np.ndarray, r: float):
        new_size = (int(img.shape[2]*r), int(img.shape[1]*r))
        img = Image.fromarray(img[0].astype(np.uint8), mode="L")
        img = img.resize(new_size, Image.BILINEAR)
        img = np.array(img, dtype=np.float32)[np.newaxis, ...]
        return img

    def __call__(self, img: Union[Image.Image, np.ndarray]):
        """
            img should be either Image or np.ndarray with C*H*W
        """
        if isinstance(img, Image.Image):
            if img.mode != "L":
                img = img.convert("L")
            img = np.array(img, dtype=np.float32)[np.newaxis, ...]  # C H W
        # self.save_img(img[0], "original.png")
        img = self.pad_resize(img)  # C H W
        # self.save_img(img[0], "pad_resize.png")
        img = self.normalize(img)  # C H W
        # self.save_img(img[0], "normalize.png")
        img = self.pad_image(img)  # C H W
        # self.save_img(img[0], "padded.png")
        return img


class PadMaxResize(object):
    __max_iter__ = 10
    def __init__(self, min_size: Tuple[int, int],  max_size: Tuple[int, int],
                 interpolation=Image.BILINEAR,):
        super(PadMaxResize, self).__init__()
        self.min_size = min_size
        self.max_size = max_size
        self.interpolation = interpolation

    def pad_resize(self, img: np.ndarray):
        _, h, w = img.shape
        img = img[0]  # C H W -> H W
        mxh, mxw = self.max_size
        mnh, mnw = self.min_size
        # height
        if h > mxh:
            ratio_h = h / mxh
        elif h < mnh:
            ratio_h = -1
        else:
            ratio_h = 1
        # width
        if w > mxw:
            ratio_w = w / mxw
        elif w < mnw:
            ratio_w =  -1
        else:
            ratio_w = 1
        if ratio_h == 1 and ratio_w == 1:
            return img
        # pad first
        if ratio_h == -1 or ratio_w == -1:
            pw = mnw - w if ratio_w == -1 else 0
            ph = mnh - h if ratio_h == -1 else 0
            # img = VF.pad(img, [0, 0, pw, ph], fill=255)
            img = np.pad(img, ((0, ph), (0, pw)), "constant", constant_values=(255,))
        if ratio_h > 1 or ratio_w > 1:
            h, w = img.shape
            ratio = max(ratio_h, ratio_w)
            size = (int(w/ratio), int(h/ratio))
            # import matplotlib.pyplot as plt
            # plt.imsave("before.png", img, cmap="gray")
            img = np.array(Image.fromarray(img.astype(np.uint8), mode="L").resize(size, self.interpolation), dtype=img.dtype)
            # plt.imsave("after0.png", img0, cmap="gray")
            # size = (int(h/ratio), int(w/ratio))
            # plt.imsave("after1.png", img1, cmap="gray")
        # H W -> C H W
        return img[np.newaxis, ...]

    def is_img_valid(self, img: np.ndarray):
        _, h, w = img.shape
        c = False
        if self.min_size[0] <= h <= self.max_size[0] and self.min_size[1] <= w <= self.max_size[1]:
            c = True
        return c

    def __call__(self, img: np.ndarray):
        # img: C H W
        if img.shape[0] != 1:
            img = np.array(Image.fromarray(img.astype(np.uint8), mode="RGB").convert("L"), dtype=np.float32)[np.newaxis, ...]
        it = 0
        while not self.is_img_valid(img) and it < self.__max_iter__:
            img = self.pad_resize(img)
            it += 1
        assert it < self.__max_iter__, f"pad_resize match the maximum iter, img size: {img.shape}"
        return img


def get_transforms(min_img_size, max_img_size):
    transforms = DeployTransform(
        min_img_size, max_img_size
    )
    return transforms


if __name__ == "__main__":
    ...
