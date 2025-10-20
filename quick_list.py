from pathlib import Path


class Database:
    def __init__(self, database_loc="./db.json", database_type="json") -> None:
        self.db = {"type": database_type, "location": Path.absolute(database_loc)}

    def load_database(): ...


class InputHandler:
    def __init__(self) -> None: ...


if __name__ == "__main__":
    main()
