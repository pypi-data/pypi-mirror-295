import os

import logging
from logging.handlers import TimedRotatingFileHandler

from lced_utils.uuid_utils import generate_uuid4


def setup_logger(uuid_str):
    logger = logging.getLogger(f"lced_logger_{uuid_str}")
    logger.setLevel(logging.DEBUG)

    project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(project_root_path, "logs", "app.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(threadName)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        log_file, when="MIDNIGHT", interval=1, backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger(generate_uuid4())
