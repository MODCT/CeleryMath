'''
Description: logger
Author: Rainyl
Date: 2022-06-07 23:36:33
LastEditTime: 2022-06-07 23:49:10
'''
import logging
from colorlog import ColoredFormatter


formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
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
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
