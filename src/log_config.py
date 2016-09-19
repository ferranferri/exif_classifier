import logging

LOG_NAME = 'IMG_SORT'


def init():
    logging.basicConfig(level=logging.CRITICAL)


def get_logger():
    global LOG_NAME
    return logging.getLogger(LOG_NAME)
