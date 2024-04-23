import logging
import os
from typing import Optional

from hardverapro_pp.utils.config import Config


def initialize(config: Config) -> None:
    log_level = config.key('logging').key('level').str('Warning')
    level = logging.getLevelName(log_level.upper())

    # HA_LOG_FILEPATH
    file_name: Optional[str] = os.environ.get('HA_LOG_FILEPATH', '')
    if not file_name:
        cfg_file_name = config.key('logging').key('path').str('')
        file_name = cfg_file_name if cfg_file_name else None

    logging.basicConfig(filename=file_name, encoding='utf-8', level=level)

    if config.key('logging').key('stdout').bool(True) is False:
        logging.getLogger(__name__).propagate = False
