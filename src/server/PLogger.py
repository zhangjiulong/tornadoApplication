#coding=utf-8
import logging
import os
from config import kLogFile


class Logger:
    dir, fileName = os.path.split(kLogFile)
    if not os.path.exists(dir):
        os.makedirs(dir)
    staticLogger = logging.getLogger('PACS')
    handler = logging.FileHandler(kLogFile)
    formatter = logging.Formatter('%(asctime)s ; [%(name)s] : [%(levelname)s] : %(message)s') #,"%Y-%m-%d ; %H:%M:%S , %f"不成功，为什么
    handler.setFormatter(formatter)

    staticLogger.addHandler(handler)
    staticLogger.setLevel(logging.INFO)

    def __init__(self):
        self._logger = Logger.staticLogger

    def info(self, msg):
        if self._logger is not None:
            self._logger.info(msg)

    def debug(self, msg):
        if self._logger is not None:
            self._logger.debug(msg)

    def warn(self, msg):
        if self._logger is not None:
            self._logger.warn(msg)

    def error(self, msg):
        if self._logger is not None:
            self._logger.error(msg)

if __name__ == '__main__':
    logger = Logger()
    logger.info('ok')
