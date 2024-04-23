# ruff: noqa: S301
import logging
import os
import pickle  # nosec B403
from pathlib import Path

from hardverapro_pp.core.ha_item import HardveraproItem


class ItemDatabase:
    def __init__(self, query_id: str) -> None:
        database_folder = os.environ.get('HA_DATABASE_FOLDER', '')
        self._logger = logging.getLogger(__name__)
        self._query_id = query_id
        self._database_path = Path(database_folder) / (query_id + '.pkl')
        self._database: list[HardveraproItem] = []
        self._database_newly_created = True
        if Path(self._database_path).exists():
            with Path(self._database_path).open('rb') as db_file:
                self._database = pickle.load(db_file)  # nosec B301
                self._database_newly_created = False
        else:
            self._logger.info(f'Created new database for: "{query_id}"')

    def is_new_database(self) -> bool:
        return self._database_newly_created

    def _save_database(self) -> None:
        with Path(self._database_path).open('wb') as f:
            pickle.dump(self._database, f)

    def exists(self, item: HardveraproItem) -> bool:
        return item in self._database

    def insert(self, item: HardveraproItem) -> None:
        self._database.append(item)
        self._save_database()

    def delete(self, item_id: str) -> bool:
        old_size = len(self._database)
        self._database = [obj for obj in self._database if obj.id != item_id]
        self._save_database()
        return len(self._database) < old_size

    def __str__(self) -> str:
        out = f'Database Id: {self._query_id}{os.linesep}'
        out += f'Database path: {self._database_path}{os.linesep}'
        out += f'Database new: {self._database_newly_created}{os.linesep}'
        for i, element in enumerate(self._database):
            element_str = str(element)
            out += f'[{i}]:{os.linesep}\t'
            out += element_str.replace(os.linesep, f'{os.linesep}\t')
            out += os.linesep
        return out
