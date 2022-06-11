from typing import List, Tuple, Union
import re


def to_2tuple(t: Union[Tuple, int]):
    return t if isinstance(t, tuple) else (t, t)


def timer(func):
    from time import time

    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        end = time()-t1
        print(f"{func.__name__} took {end:.2f}s")
        return result
    return wrapper


def seed_everything(seed: int):
    """
        from https://gist.github.com/ihoromi4/b681a9088f348942b01711f251e5f964
        thanks!
    """
    import random, os
    import numpy as np
    
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)


def post_process(s: str):
    """
        modified from https://github.com/lukas-blecher/LaTeX-OCR, thanks!
        Remove unnecessary whitespace from LaTeX code.
        Args:
            s (str): Input string
        Returns:
            str: Processed latex string
    """
    text_reg = r'(\\(operatorname|mathrm|text|mathbf)\s?\*? {.*?})'
    letter = '[a-zA-Z]'
    noletter = '[\W_^\d]'
    names = [x[0].replace(' ', '') for x in re.findall(text_reg, s)]
    s = re.sub(text_reg, lambda match: str(names.pop(0)), s)
    news = s
    while True:
        s = news
        news = re.sub(r'(?!\\ )(%s)\s+?(%s)' % (noletter, noletter), r'\1\2', s)
        news = re.sub(r'(?!\\ )(%s)\s+?(%s)' % (noletter, letter), r'\1\2', news)
        news = re.sub(r'(%s)\s+?(%s)' % (letter, noletter), r'\1\2', news)
        if news == s:
            break
    return s


if __name__ == '__main__':
    ...
