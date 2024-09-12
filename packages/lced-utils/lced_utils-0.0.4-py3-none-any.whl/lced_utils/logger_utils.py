import os

import logging
from logging.handlers import TimedRotatingFileHandler

from lced_utils.buffer_utils import get_project_root_path, get_project_logging


def setup_logger():
    log_file = os.path.join(get_project_root_path(), "logs", "app.log")
    log_level_str = get_project_logging().get("level", "").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(threadName)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            TimedRotatingFileHandler(
                log_file, when="MIDNIGHT", interval=1, backupCount=7
            ),
        ],
    )
