from __future__ import annotations

import logging
import os
from typing import Optional, Type, TypeVar

import yaml


class Config:
    def __init__(self, config: Optional[tuple[dict, str]] = None) -> None:
        if config:
            self._config = config[0]
            self._config_name = config[1]
            return

        self._config = {}
        self._config_name = "root"
        self._logger = logging.getLogger(__name__)
        config_path = os.environ.get("HA_CONFIG_FILEPATH", "cfg/config.yml")

        try:
            with open(config_path, "r", encoding="utf-8") as file:
                self._config = yaml.safe_load(file.read())
        except Exception as e:
            self._logger.error(f'Failed to open config file at: "{config_path}"')
            raise e

    def key(self, key: str) -> Config:
        if key not in self._config:
            return Config(({}, key))

        return Config((self._config[key], key))

    T = TypeVar("T")

    def _val(self, type_value: Type[T], default: Optional[T] = None) -> T:
        try:
            if isinstance(self._config, dict) or not self._config:
                raise TypeError(f"Config is a {type(self._config)}, which is not meant to be converted into {str(type_value)}")
            return type_value(self._config)
        except (ValueError, TypeError) as e:
            if default is not None:
                return default

            self._logger.error(f'Error, getting config key "{self._config_name}". Conversion couldn\'t be done: {str(e)}')
            raise e

    def int(self, default: Optional[int] = None) -> int:
        return self._val(int, default)

    def str(self, default: Optional[str] = None) -> str:
        return self._val(str, default)

    def bool(self, default: Optional[bool] = None) -> bool:
        return self._val(bool, default)

    def list(self, default: Optional[list[Config]] = None) -> list[Config]:
        if not isinstance(self._config, list):
            if default is not None:
                return default
            error_message = f'Error, getting config key "{self._config_name}". Conversion couldn\'t be done from {type(self._config)} to list[]'
            self._logger.error(error_message)
            raise Exception(error_message)

        return [Config((item, self._config_name)) for item in self._config]
