'''
Description: logger
Author: Rainyl
Date: 2022-06-07 23:36:33
LastEditTime: 2022-06-14 12:58:07
'''
import logging
import os
from colorlog import ColoredFormatter


formatter = ColoredFormatter(
    "%(name)s_%(log_color)s%(levelname)s%(reset)s_%(module)s_%(purple)s%(lineno)d_%(blue)s%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%',
)


def get_logger(name, level=logging.DEBUG):
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if not os.path.exists("log"):
        os.mkdir("log")
    file_handler = logging.FileHandler("log/celeryMath.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
    return logger
