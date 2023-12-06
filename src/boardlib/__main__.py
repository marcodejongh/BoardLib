import argparse
import csv
import getpass
import pyperclip
import sys

import boardlib.api.aurora
import boardlib.api.moon


LOGBOOK_FIELDS = (
    "board",
    "angle",
    "name",
    "date",
    "grade",
    "tries",
)


def logbook_entries(board, username, password, grade_type="font"):
    api = (
        boardlib.api.moon
        if board.startswith("moon")
        else boardlib.api.aurora
        if board in boardlib.api.aurora.HOST_BASES
        else None
    )
    if api:
        yield from api.logbook_entries(board, username, password, grade_type)

    else:
        raise ValueError(f"Unknown board {board}")


def write_entries(output_file_path, entries, no_headers=False):
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, LOGBOOK_FIELDS)
    if not no_headers:
        writer.writeheader()

    writer.writerows(entries)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "board",
        help="Board name",
        choices=sorted(
            boardlib.api.moon.BOARD_IDS.keys() | boardlib.api.aurora.HOST_BASES.keys()
        ),
    )
    parser.add_argument("-u", "--username", help="Username", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=False)
    parser.add_argument(
        "--no-headers", help="Don't write headers", action="store_true", required=False
    )
    parser.add_argument(
        "-g",
        "--grade-type",
        help="Grade type",
        choices=("font", "hueco"),
        default="font",
        required=False,
    )
    args = parser.parse_args()

    password = pyperclip.paste()
    password = getpass.getpass("Password: ")
    entries = logbook_entries(args.board, args.username, password, args.grade_type)

    if args.output:
        write_entries(args.output, entries, args.no_headers)
    else:
        with open(sys.stdout.fileno(), mode='w', encoding='utf-8', newline='') as stdout_file:
            write_entries(stdout_file, entries, args.no_headers)


if __name__ == "__main__":
    main()
