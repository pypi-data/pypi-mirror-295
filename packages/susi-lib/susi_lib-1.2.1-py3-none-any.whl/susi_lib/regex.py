"""Provides RegEx class for better work with regular expressions, create_regex function to create
a RegEx instance based without the full knowledge of regular expression syntax.
"""

import re
from enum import Enum, auto


class RegEx:
    """Class to store and execute a regular expression on some provided data."""

    def __init__(self, pattern: str, data: list[str] | str | None = None):
        """Create RegEx instance.

        :param pattern: Valid regular expression pattern
        """
        if not isinstance(pattern, str):
            raise TypeError("Pattern needs to be a string")
        try:
            self.__re = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
        except Exception as e:
            raise ValueError("Invalid regex pattern: " + str(e)) from e
        if data is not None:
            self.set_data(data)

    def set_data(self, data: list[str] | str):
        """Sets data on which the regular expression will execute.

        :param data: String containing a filename or a list[str] containing wanted data
        """
        if isinstance(data, str):
            with open(data, "r", encoding="utf-8") as f:
                self.__data = []
                for line in f:
                    self.__data.append(line.strip())
        elif isinstance(data, list):
            self.__data = data
        else:
            raise TypeError(
                "Data must be a string with filename or list[str] with some data"
            )

    def execute(self):
        """Executes the regular expression on provided data. Need to provide data first.

        :return: List of all found matches
        """
        if self.__data is None:
            raise AttributeError("Did not set data to search before search")

        input_text = "\n".join(self.__data)
        return self.__re.findall(input_text)

    def get_pattern(self):
        """Returns the regular expression pattern.

        :return: RE pattern
        """
        return self.__re.pattern


class Selection(Enum):
    """Enum to specify what to do with a set of characters when creating RE by create_regex."""

    NONE = auto()
    """Don't do anything"""
    INVERT = auto()
    """Invert the set"""
    ANY = auto()
    """Override this set to match any character"""


def create_regex(
    *args: tuple[str, Selection],
    data: list[str] | str | None = None,
    length: int | tuple[int, int] = None,
    letters: str = None,
    invert: bool = False,
) -> RegEx:
    """Creates a RegEx object from arguments.

    If args is specified, it will loop through it and create a pattern. Each tuple contains a set
    of character and enum to specify what to do with it. Sets of characters are by default wanted.
    The length of the wanted words will be the numbers of tuples provided.

    If args is not specified, it will use remaining keyword arguments to create a RegEx object.
    Length determines length of the words, letters a set of wanted letters and invert wether to
    turn wanted letters into unwanted.
    :param args: Set of wanted characters and enum to specify special action.
    :param length: Int specifying length of the word or a pair (begin, end) specifying a range
    :param letters: Set of wanted letters
    :param invert: Bool value, set to True to turn wanted letters to unwanted
    :return: RegEx object with desired pattern
    """
    if len(args) > 0:
        pattern = "^"
        for position in args:
            if (
                len(position) != 2
                or not isinstance(position[0], str)
                or not isinstance(position[1], Selection)
            ):
                raise TypeError("All arguments must be tuples (str, Selection)")
            part = position[0]
            match (position[1]):
                case Selection.NONE:
                    if len(part) == 0:
                        raise ValueError("Set of letters can't be empty")
                    part = f"[{part}]"
                case Selection.INVERT:
                    if len(part) == 0:
                        raise ValueError("Set of letters can't be empty")
                    part = f"[^{part}]"
                case Selection.ANY:
                    part = "."
                case _:
                    raise ValueError("Invalid enum value")
            pattern += f"{part}"
        pattern += "$"
        return RegEx(pattern, data)
    if length is None or letters is None:
        raise ValueError("You must set all arguments")
    if not isinstance(length, (int, tuple)):
        raise TypeError("Length must an int or pair (int, int)")
    if not isinstance(letters, str):
        raise TypeError("Letters must be a string")
    if not isinstance(invert, bool):
        raise TypeError("Invert must be a bool")
    inv = "^" if invert else ""
    quantify = (
        f"{{{length}}}" if isinstance(length, int) else f"{{{length[0]},{length[1]}}}"
    )
    pattern = f"^[{inv}{letters}]{quantify}$"
    return RegEx(pattern, data)
