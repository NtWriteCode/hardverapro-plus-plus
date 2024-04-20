import os
import pickle
from hardverapro_pp.core.ha_query import HardveraproQuery
from hardverapro_pp.core.ha_item import HardveraproItem


class ItemDatabase:
    def __init__(self, query_id: str) -> None:
        database_folder = os.environ.get('HA_DATABASE_FOLDER', '')
        self._database_path = os.path.join(database_folder, query_id + '.pkl')
        self._database: list[HardveraproItem] = []
        self._database_newly_created = True
        if os.path.exists(self._database_path):
            self._database = pickle.load(self._database_path)
            self._database_newly_created = False
        else:
            print(f'Created new database for: "{query_id}"')

    def is_new_database(self) -> bool:
        return self._database_newly_created

    def _save_database(self) -> None:
        with open(self._database_path, 'wb') as f:
            pickle.dump(self._database, f)

    def exists(self, item: HardveraproItem) -> bool:
        return item in self._database

    def insert(self, item: HardveraproItem) -> None:
        self._database.append(item)
        self._save_database()
