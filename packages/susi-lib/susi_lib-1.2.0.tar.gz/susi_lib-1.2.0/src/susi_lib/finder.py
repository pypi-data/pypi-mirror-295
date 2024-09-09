"""Contains the Finder class for searching in text."""

from typing import Callable, List, Literal, Union, overload


class Finder:
    """Class for finding words that satisfy all user provided functions.

    Supports lazy iteration over all matches.
    """

    def __init__(self, inp: Union[str, List[str]], *functions: Callable[[str], bool]):
        """Creates new Finder instance.

        :param inp: Input data. Either a filename or a list[str] containing lines
        :param functions: Functions that will determine wether a word is wanted or not
        """
        if isinstance(inp, str):
            with open(inp, "r", encoding="utf-8") as f:
                self.__text = []
                for line in f:
                    self.__text.append(line.strip())
        elif isinstance(inp, list):
            self.__text = inp
        else:
            raise TypeError(
                "Inp must be a string with filename or list[str] with some data"
            )
        for f in functions:
            if not isinstance(f, Callable):
                raise TypeError("All functions must be callable")
        self.__function = list(functions)

    def __valid_word(self, word: str):
        for f in self.__function:
            if not f(word):
                return False
        return True

    @overload
    def __execute(self, first: Literal[True]) -> Union[str, None]: ...

    @overload
    def __execute(self, first: Literal[False]) -> List[str]: ...

    def __execute(self, first: bool):
        result = []
        for word in self.__text:
            if self.__valid_word(word):
                if first:
                    return word
                result.append(word)
        return result if not first else None

    def __iter__(self):
        for word in self.__text:
            if self.__valid_word(word):
                yield word

    def find_first(self):
        """Finds the first occurrence of a valid word and returns it.

        :return: The found word or None if no valid words are found
        """
        return self.__execute(True)

    def find_all(self):
        """Finds all occurrences of a valid words and returns them.

        :return: List of found valid words
        """
        return self.__execute(False)

    def change_function(self, *functions: Callable[[str], bool]):
        """Changes functions for other functions.

        :param functions: New list of functions
        """
        for f in functions:
            if not isinstance(f, Callable):
                raise TypeError("All functions must be callable")
        self.__function = list(functions)

    def add_function(self, *functions: Callable[[str], bool]):
        """Adds new functions to constraint valid words.

        :param functions: New functions to add
        """
        for f in functions:
            if not isinstance(f, Callable):
                raise TypeError("All functions must be callable")
        self.__function.extend(functions)
