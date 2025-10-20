# Not using anything fancy

import json


def read_json(file) -> list:
    file = open(file, "r")
    data = json.load(file)
    file.close()
    return data


def write_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


def get_entry_list() -> list[str]:
    new_inputs: list[str] = []
    new_entry = ""
    while True:
        new_entry = input("- ").lower()
        if new_entry == "":
            break
        new_inputs.append(new_entry)
    return new_inputs


def add(db):
    print("Please enter a name/title to save:")
    new_inputs = get_entry_list()
    data = read_json(db)
    data += new_inputs
    write_json(db, data)


def read_file(db):
    file_to_read = input("Enter file to load: ")
    new_inputs = []
    with open(file_to_read, "r") as f:
        data = f.read().split("\n")
        new_inputs = list(filter(None, data))

    write_json(db, list(set(read_json(db) + new_inputs)))


def delete(db):
    print("Existing entries:")
    view(db)
    print("Enter entries to delete:")

    data = read_json(db)
    marked_entries = get_entry_list()
    if "*" in marked_entries:
        new_data = []
    else:
        new_data = [entry for entry in data if entry not in marked_entries]
    write_json(db, new_data)


def view(db):
    data = read_json(db)
    if len(data) == 0:
        print("Database is empty")
    for entry in data:
        print("-", entry)


def main():
    db = "db.json"
    while True:
        mode = input("Select mode: [a]dd, [r]ead a file, [d]elete, [v]iew, [q]uit: ")
        match mode:
            case "a":
                add(db)
            case "r":
                read_file(db)
            case "d":
                delete(db)
            case "v":
                view(db)
            case "q":
                return
            case _:
                print("No valid command selected, quitting")
                return


if __name__ == "__main__":
    main()
