"""
Module with custom logger configuration.
"""
import logging

LOG_MESSAGE_FORMAT = "[%(name)s] [%(asctime)s] %(message)s"

LOG_DATE_FORMAT = "%Y-%m-%dT%T"


class CustomHandler(logging.StreamHandler):
    def __init__(self) -> None:
        super().__init__()
        formatter = logging.Formatter(fmt=LOG_MESSAGE_FORMAT, datefmt=LOG_DATE_FORMAT)
        self.setFormatter(fmt=formatter)


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name=name)

    logger.setLevel(level=level)
    logger.addHandler(hdlr=CustomHandler())

    return logger
