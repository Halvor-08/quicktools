from database import Database


def handle(args, db: Database):
    entries = db.dump_db()
    for entry in entries:
        print(entry)
