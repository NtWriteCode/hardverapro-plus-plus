#!/usr/local/bin/python3

import os
import argparse
from pathlib import Path
from hardverapro_pp.utils.database import ItemDatabase
from hardverapro_pp.utils.config import Config

def list_items():
    database_folder = os.environ.get('HA_DATABASE_FOLDER', '.')
    pkl_files = list(Path(database_folder) .glob('*.pkl'))

    for file in pkl_files:
        database = ItemDatabase(file.stem)
        print(database)


def delete_item(item_id):
    print(f"Deleting item with ID {item_id}...")

def main():
    parser = argparse.ArgumentParser(description="HardverApro CLI tool")
    parser.add_argument("action", choices=["list", "delete"], help="Action to perform on the database: list or delete")
    parser.add_argument("--item_id", type=int, help="ID of the item to delete")

    args = parser.parse_args()
    cfg = Config()
    
    if args.action == "list":
        list_items()
    elif args.action == "delete":
        if args.item_id is None:
            parser.error("Please provide the item ID to delete")
        delete_item(args.item_id)

if __name__ == "__main__":
    main()
