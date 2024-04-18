import os
import pickle
from ha_query import HardveraproQuery
from ha_item import HardveraproItem


class ItemDatabase:
    def __init__(self, query: HardveraproQuery) -> None:
        self._database_name = query.id + '.pkl'
        self._database: list[HardveraproItem] = []
        self._database_newly_created = True
        if os.path.exists(self._database_name):
            self._database = pickle.load(self._database_name)
            self._database_newly_created = False

    def is_new_database(self) -> bool:
        return self._database_newly_created

    def save_database(self) -> None:
        with open(self._database_name, 'wb') as f:
            pickle.dump(self._database, f)

    def exists(self, item: HardveraproItem) -> bool:
        return item in self._database

    def insert(self, item: HardveraproItem) -> None:
        self._database.append(item)
        self.save_database()
