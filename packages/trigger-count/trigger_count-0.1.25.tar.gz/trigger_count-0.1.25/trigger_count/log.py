"""Handle logging."""
import logging
import sys
from pathlib import Path


def get_file_logger(name: str, file_path: Path) -> logging.Logger:
    logger = get_basic_logger(name)
    file_handler = logging.FileHandler(file_path)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def get_basic_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger