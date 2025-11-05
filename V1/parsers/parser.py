"""
Parser module, implements basic parsing of arguments.

    MODES
    - Adding: Adding an entry or multiple entries
    - Lookup: View database and lookup specific entry
"""

import argparse
from sys import argv
from commands import view, add, find, delete


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Quicktool library",
        description="Description",
        epilog="Something at the end, like hey my name is X",
    )
    parser.add_argument("--db", default="json", choices=["json", "db"])
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "-f", "--force", help="Forces every action, skipping ALL confirmation"
    )

    subparsers = parser.add_subparsers(dest="mode", required=True)

    view_parser = subparsers.add_parser("view")
    view_parser.set_defaults(func=view.handle)
    view_parser.add_argument(
        "-l", "--length", type=int, help="Number of entries to print"
    )

    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("-t", "--title", required=True)
    find_parser.add_argument("-a", "--artist", required=True)
    find_parser.add_argument("-b", "--album")
    find_parser.set_defaults(func=find.handle)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("-t", "--title", required=True)
    add_parser.add_argument("-a", "--artist", required=True)
    add_parser.add_argument("-b", "--album")
    add_parser.add_argument(
        "-n",
        "--note",
        help="Notes are saved to the highest specificity available.\nThis means that the note is appended to the first item present, in order: Song, Album, Artist",
    )
    add_parser.set_defaults(func=add.handle)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.set_defaults(func=delete.handle)
    delete_parser.add_argument("--all", help="Deletes the entire database")

    # Default to view mode when no mode provided
    # Hacky, but best current solution with argparse
    if len(argv) == 1:
        argv.append("view")

    return parser
