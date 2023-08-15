"""
Description: logger
Author: Rainyl
Date: 2022-06-07 23:36:33
LastEditTime: 2022-06-14 12:58:07
"""
import logging

import coloredlogs


class CeleryLogger(logging.Logger):
    def __init__(self, name: str, level=logging.DEBUG):
        super(CeleryLogger, self).__init__(name=name, level=level)
        coloredlogs.install(level='DEBUG', logger=self)
