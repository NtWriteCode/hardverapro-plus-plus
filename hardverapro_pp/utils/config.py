from __future__ import annotations
from typing import Type, TypeVar
import yaml
import os

class Config:
    def __init__(self, config: tuple[object, str] = None) -> None:
        if config:
            self.config = config[0]
            self.config_name = config[1]
            return
        
        self.config = {}
        self.config_name = 'root'
        config_path = os.environ.get('HA_CONFIG_PATH', 'cfg/config.yml')

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file.read())
        except Exception:
            print(f'Failed to open config file at: "{config_path}"')

    def key(self, key: str) -> Config:
        if key not in self.config:
            return Config(({}, key))

        return Config((self.config[key], key))

    T = TypeVar('T')
    def val(self, type_value: Type[T], default: T = None) -> T:
        try:
            return type_value(self.config)
        except (ValueError, TypeError) as e:
            if default:
                return default
            
            print(f'Error, getting config key "{self.config_name}". Conversion couldn\'t be done: {str(e)}')
            return None

    def int(self, default: int = None) -> int:
        return self.val(int, default)

    def str(self, default: str = None) -> str:
        return self.val(str, default)

    def list(self, default: object = None) -> list[Config]:
        if not isinstance(self.config, list):
            if default:
                return default
            print(f'Error, getting config key "{self.config_name}". Conversion couldn\'t be done from {type(self.config)} to list[]')

        return [Config((item, self.config_name)) for item in self.config]
