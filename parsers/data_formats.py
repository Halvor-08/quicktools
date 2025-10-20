from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# Frontend classes
@dataclass
class UserEntry:
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    note: Optional[str] = None

    def __post_init__(self):
        if not any((self.title, self.album, self.artist)):
            print(
                "[USER ENTRY PROCESSING ERROR]\nCannot generate valid entry: No title, album title or artist provided."
            )

    def unpack(self):
        return self.artist, self.title, self.album, self.note


# Storage classes
@dataclass
# Different types of notes? (Todos and general comments/notes/reminders) -> Later version
class Note:
    raw_text: str
    entry_date: Optional[datetime] = None

    def __post_init__(self):
        if isinstance(self.entry_date, str):
            self.entry_date = datetime.fromisoformat(self.entry_date)
        elif not self.entry_date:
            self.entry_date = datetime.now().isoformat()

    def __str__(self):
        if not self.raw_text:
            return ""
        date_str = self.entry_date.strftime("%y/%m/%d %H:%M") if self.entry_date else ""
        return f"[{date_str}] {self.raw_text}"


@dataclass
class BaseEntry:
    title: str
    note: Optional[Note | list[Note]] = None

    def __post_init__(self):
        if not self.note:
            return
        if isinstance(self.note, Note):
            self.note = [self.note]

    def add_note(self, new_note: Note):
        if not self.note:
            self.note = [new_note]
        else:
            self.note.append(new_note)

    def __str__(self) -> str:
        return_str = self.title
        if self.note:
            return_str += f": {self.note}"
        return return_str


@dataclass
class Song(BaseEntry): ...


@dataclass
class Album(BaseEntry):
    songEntries: list[Song] = None

    def __str__(self) -> str:
        return_str = super().__str__()
        for elem in self.songEntries:
            return_str += f"\n\t{elem.__str__()}"
        return return_str


@dataclass
class Artist(BaseEntry):
    singles: list[Song] = None
    albums: list[Album] = None

    def __str__(self) -> str:
        return_str = super().__str__()

        if self.albums:
            return_str += f"\n  Album{'s' if len(self.albums) > 1 else ''}:"
            for elem in self.albums:
                return_str += f"\n\t{elem.title}"
                if elem.note:
                    return_str += f": {elem.note}"

        if self.singles:
            return_str += f"\n  Single{'s' if len(self.singles) > 1 else ''}:"
            for elem in self.singles:
                return_str += f"\n\t{elem.__str__()}"

        return return_str


# TODO:
# Figure out merging of existing and new classes for all levels (base class function?)
# Write function to parse these classes
# DONT FORGET: These are dataclasses, if they need to be changed to classes do so
