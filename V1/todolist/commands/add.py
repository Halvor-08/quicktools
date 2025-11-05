from database import Database
import data_formats


def handle(args, db: Database):
    new_entry = data_formats.UserEntry(args.title, args.artist, args.album, args.note)
    db.add_entry(new_entry)
