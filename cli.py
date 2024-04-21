#!/usr/local/bin/python3

import argparse
import os
from pathlib import Path

from hardverapro_pp.utils.database import ItemDatabase


def list_item(database_id: str, item_id: str):
    file_selector = "*" if database_id == None else database_id
    database_folder = os.environ.get("HA_DATABASE_FOLDER", ".")
    pkl_files = list(Path(database_folder).glob(file_selector + ".pkl"))

    for file in pkl_files:
        database = ItemDatabase(file.stem)
        if item_id:
            print(f"Database Id: {database._query_id}")
            print(f"Database path: {database._database_path}")
            print(f"Database new: {database._database_newly_created}")
            i = 0
            for element in database._database:
                if element.id == item_id:
                    element_str = str(element)
                    print(f"[{i}]:{os.linesep}")
                    print("\t" + element_str.replace(os.linesep, f"{os.linesep}\t"))
                    print()
                    i += 1
        else:
            print(database)


def delete_item(database_id: str, item_id: str):
    if database_id == None and item_id == None:
        print("At least database id or item id must be defined!")
        return

    file_selector = "*" if database_id == None else database_id
    database_folder = os.environ.get("HA_DATABASE_FOLDER", ".")
    pkl_files = list(Path(database_folder).glob(file_selector + ".pkl"))

    for file in pkl_files:
        if item_id:
            database = ItemDatabase(file.stem)
            succeed = database.delete(item_id)
            if succeed:
                print(f"{file.stem}.{item_id} is successfully deleted.")
        else:
            file.unlink()
            print(f"{file.stem} is successfully deleted.")


def main():
    parser = argparse.ArgumentParser(description="HardverApro++ CLI tool")
    parser.add_argument(
        "action",
        choices=["list", "delete"],
        help="Action to perform on the database: list or delete",
    )
    parser.add_argument("-i", "--item_id", type=str, help="Id of the item to interact with")
    parser.add_argument("-d", "--database_id", type=str, help="Database Id to use for delete action")

    args = parser.parse_args()

    if args.action == "list":
        list_item(args.database_id, args.item_id)
    elif args.action == "delete":
        delete_item(args.database_id, args.item_id)


if __name__ == "__main__":
    main()
