import json
from rapidfuzz import process
from dataclasses import dataclass


@dataclass
class EntryField:
    key_name: str
    data_type: type
    input_type: type


class Entry:
    def __init__(self, top_row_db) -> None:
        self.template = self.return_type(top_row_db)

    def normalize_types(self, origin_type) -> type:
        if type(origin_type) in (str, int, float, bool):
            return type(origin_type)
        else:
            return bytes

    def return_type(self, top_row_db) -> list[EntryField]:
        """
        Returns a list of dicts describing the datatypes for entries
        Each dict in the list contains the following pairs:
        1. "key_name": [str] name of the key described in the dict
        2. "data_type": [any] type of the actual loaded data
        3. "input_type": [any] describes the type of data contained
        """
        # TODO: finalize whether to actually use this...

        type_list = []
        for elem in top_row_db.keys():
            type_list.append(EntryField(elem, type(elem), self.normalize_types(elem)))
        return type_list


class DataBackend:
    # TODO:
    # - Add settings
    #   - limit
    #   - DB type and path
    # - Dynamically load datatype (define entry) from db return
    def __init__(self) -> None:
        self.db = DataBase()
        # Assuming DB stays small enough to live load into memory
        self.data: list[dict[str, str]] = self.db.load_data()
        self.entry_template = Entry(self.data[0]).template

    def search(self, query, limit=20) -> list[dict]:
        # TODO:
        # - lowercase all unless capital letter is present in query
        # - Seems oversensitive on adding new chars?
        if not query:
            return self.data[:limit]

        results = process.extract(
            query=query, choices=self.data, processor=lambda x: x["name"], limit=limit
        )
        return [x[0] for x in results]

    def add_entry(self, new_entry: Entry):
        pass

    def delete_entry(self, entry: Entry):
        """
        Deletes entry in the database
        Entry MUST be in the database, using exact "primary" match
        """
        pass


class JSONDataBase: ...


class SQLDataBase: ...


class DataBase:
    """
    Very simplistic database class
    Reads and writes from json file with no validation

    Handles database interaction and low-level manipulation
    TODO:
        - Path validation using pathlib
        - settings/argument handler for other location
        - proper db?
    """

    # TODO:
    # - Add JSON subclass

    def __init__(self) -> None:
        self.db = {"type": "json", "path": "db.json"}

    def read_json(self) -> list[dict]:
        file = open(self.db["path"], "r")
        data = json.load(file)
        file.close()
        return data

    def write_json(self, data) -> None:
        """
        Writes raw data to self.db['path']
        """
        with open(self.db["path"], "w") as file:
            json.dump(data, file)

    def load_data(self) -> list[dict]:
        return self.read_json()


if __name__ == "__main__":
    DataBackend()
