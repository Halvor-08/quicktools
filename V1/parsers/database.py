from dataclasses import asdict
import os
import json
from data_formats import Artist, Album, Song, Note, UserEntry


class Database:
    def init_db(self):
        raise NotImplementedError

    def add_entry(self, entry):
        print(entry)
        raise NotImplementedError

    def find_entry(self, entry):
        print(entry)
        raise NotImplementedError

    def view_entry(self, entry):
        print(entry)
        raise NotImplementedError

    def dump_db(self) -> list[Artist]:
        print("Call to dump database")
        raise NotImplementedError

    def delete_entry(self, entry: UserEntry):
        print("Call to delete", entry)
        raise NotImplementedError


class JsonDatabase(Database):
    def __init__(self, file_path=None) -> None:
        self.file_path = file_path or "./storage.json"
        if not os.path.exists(self.file_path):
            self.init_db()

        self.data = self._load()
        assert self.data

    def init_db(self):
        with open(self.file_path, "w") as f:
            json.dump({}, f, indent=2)

    def _parse_note(self, note_field, date_field) -> Note | None:
        if note_field:
            return Note(note_field, date_field)
        return None

    def _parse_songs(self, json_dump):
        if not json_dump:
            return []
        return [
            Song(
                elem.get("title"), self._parse_note(elem.get("note"), elem.get("date"))
            )
            for elem in json_dump
        ]

    def _parse_albums(self, json_dump):
        if not json_dump:
            return []
        return [
            Album(
                elem.get("title"),
                self._parse_note(elem.get("note"), elem.get("date")),
                self._parse_songs(elem.get("songEntries", [])),
            )
            for elem in json_dump
        ]

    def _parse_json(self, json_dump):
        data: list[Artist] = []
        for elem in json_dump:
            data.append(
                Artist(
                    title=elem.get("title"),
                    note=elem.get("note"),
                    singles=self._parse_songs(elem.get("singles")),
                    albums=self._parse_albums(elem.get("albums")),
                )
            )
        return data

    def _load(self):
        with open(self.file_path, "r") as f:
            try:
                return self._parse_json(json.load(f))
            except json.JSONDecodeError:
                print("Error reading JSON file, exitting")
                exit(1)

    def _save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    def _log(self, message: str, level: int):
        if self.verbose >= level:
            print(message)

    def add_entry(self, entry: UserEntry):
        self.data = self._load()
        title, artist_name, album_name, note = entry.unpack()
        print(title)
        # Find or create artist
        artist = next(
            (a for a in self.data if a.title.lower() == artist_name.lower()), None
        )
        if not artist:
            artist = Artist(artist_name, None, [], [])
        print(artist)

        # Bottom-up, puts note at highest specificity
        if title:
            song = next(
                (a for a in artist.singles if a.title.lower() == title.lower()), None
            )
            if not song:
                song = Song(title, note)
            else:
                song.add_note(note)
            note = None
        if album_name:
            album = next(
                (a for a in artist.albums if a.title.lower() == album_name.lower()),
                None,
            )
            if not album:
                album = Album(title, note, [])
                artist.albums.append(album)
            else:
                album.add_note(note)
            note = None
            album.songEntries.append(None or song)
        else:
            artist.singles.append(None or song)

        if not artist:
            artist.add_note(note)
        self.data.append(artist)

        json_data = [asdict(a) for a in self.data]

        print(json_data)
        confirm = input("Save this entry? [y/N]\n")
        if confirm == "y":
            self._save(json_data)
        else:
            print("Not saving entry, exitting")

    def find_entry(self, entry: UserEntry):
        print(entry)
        title, artist_name, album_name, note = entry.unpack()

        artist = next(
            (a for a in self.data if a.title.lower() == artist_name.lower()), None
        )

        try:
            result = artist[album_name]
            print(result)
        except TypeError:
            result = None

    def view_entry(self, entry: UserEntry): ...
    def dump_db(self):
        return self.data

    def delete_entry(self, entry: UserEntry):
        title, artist_name, album_name, note = entry.unpack()

        artist = next(
            (a for a in self.data if a.title.lower() == artist_name.lower()), None
        )

        if artist:
            print(f"Found artist {artist}")

    # def store_data(self, entry):
    #     # TODO: Persistent storage handling
    #     # 1.x: Using class(?)
    #     # 2.x: Implementing DB
    #     title = entry["title"]
    #     artist = entry["artist"]
    #     album = entry["album"]
    #
    #     with open(self.default_storage_file, "w") as file:
    #         if not self.data or artist not in self.data.keys():
    #             print("Adding new artist", artist)
    #             self.data = {} if self.data is None else self.data
    #             self.data[artist] = {"singles": []}
    #
    #         if album:
    #             if album not in self.data[artist]:
    #                 self.data[artist][album] = []
    #             if title not in self.data[artist][album]:
    #                 self.data[artist][album].append(title)
    #         elif title not in self.data[artist]["singles"]:
    #             self.data[artist]["singles"].append(title)
    #         json.dump(self.data, file, indent=4)
    #         print(self.data)

    def clear_db(self):
        if (
            input(
                f"WARNING: This will delete all data in the persistent storage file {self.storage_file}\nAre you sure you want to do this? [y/N]: "
            ).lower()
            == "y"
        ):
            print("Deleting db")
