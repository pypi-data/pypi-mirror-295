import argparse
import sys
from typing import TextIO, Tuple, Union

from susi_lib.regex import Selection, create_regex


def _validate_input(wanted_letters: list[str], length: str | None):
    if len(wanted_letters) < 1:
        return False, "No wanted letters"
    if length is None:
        length = str(len(wanted_letters))
    match (length.split("-")):
        case [wl]:
            if not wl.isdigit():
                return False, "Length should be a number"
            if len(wanted_letters) not in (1, int(wl)):
                return False, "Wanted letters has wrong format"
        case [begin, end]:
            if not begin.isdigit() or not end.isdigit():
                return False, "Begin and end should be numbers"
            if len(wanted_letters) != 1:
                return False, "Wanted letters has wrong format"
        case _:
            return False, "Length has wrong format"
    return True, ""


def _translate(
    wanted_letters: list[str], length: Union[int, Tuple[int, int]], file: TextIO
):
    data = list(file)

    match len(wanted_letters):
        case 1:
            wl = wanted_letters[0]
            return ([], {"data": data, "length": length, "letters": wl})
        case _:
            args = []
            for group in wanted_letters:
                if "." in group:
                    args.append((group, Selection.ANY))
                elif group[0] == "^":
                    args.append((group[1:], Selection.INVERT))
                else:
                    args.append((group, Selection.NONE))
            return (args, {"data": data})


def main():
    arg_parser = argparse.ArgumentParser(
        description="Program for finding words using regular expressions."
    )
    arg_parser.add_argument(
        "-w", "--word-length", type=str, help="search for words of this length"
    )
    arg_parser.add_argument(
        "-i", "--input-file", type=argparse.FileType(), default=sys.stdin
    )
    arg_parser.add_argument(
        "wanted_letters",
        help="type wanted letters without spaces or space separated groups of wanted \
              letters for that position",
        nargs="*",
    )
    args = arg_parser.parse_args()

    valid, message = _validate_input(args.wanted_letters, args.word_length)
    if not valid:
        print(f"Error: {message}")
        sys.exit(1)

    word_length = (
        tuple(map(int, args.word_length.split("-")))
        if args.word_length is not None
        else len(args.wanted_letters[0])
    )
    word_length = (
        word_length[0]
        if not isinstance(word_length, int) and len(word_length) == 1
        else word_length
    )

    args, kwargs = _translate(args.wanted_letters, word_length, args.input_file)
    regex = create_regex(*args, **kwargs)
    print("\n".join(regex.execute()))
