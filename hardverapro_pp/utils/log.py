import logging
from typing import Optional


def initialize(log_level: Optional[str], log_file: Optional[str], log_to_stdout: bool) -> None:
    level = None
    file_name = None

    if log_level:
        level = logging.getLevelName(log_level.upper())

    if log_file:
        file_name = log_file

    logging.basicConfig(filename=file_name, encoding="utf-8", level=level)

    if not log_to_stdout:
        logger = logging.getLogger(__name__)
        logger.propagate = False
