"""Provides Braille class for work with braille."""


class BrailleChar:
    """Represent a single char in braille."""

    __symbol_dict = {
        "a": 0x1,
        "b": 0x3,
        "c": 0x9,
        "d": 0x19,
        "e": 0x11,
        "f": 0xB,
        "g": 0x1B,
        "h": 0x13,
        "i": 0xA,
        "j": 0x1A,
        "k": 0x5,
        "l": 0x7,
        "m": 0xD,
        "n": 0x1D,
        "o": 0x15,
        "p": 0xF,
        "q": 0x1F,
        "r": 0x17,
        "s": 0xE,
        "t": 0x1E,
        "u": 0x25,
        "v": 0x27,
        "w": 0x37,
        "x": 0x2D,
        "y": 0x3D,
        "z": 0x35,
        " ": ord(" ") - 0x2800,
    }

    def __init__(self, character):
        if not isinstance(character, str):
            raise TypeError
        if len(character) > 1 or (not character.isalpha() and character != " "):
            raise ValueError
        self.__char = character.lower()

    def __getitem__(self, item) -> bool:
        if 1 > item or item > 6:
            raise IndexError("Index must be from 1-6")
        if self.__char == " ":
            return False
        return (self.__symbol_dict[self.__char] >> (item - 1)) % 2 == 1

    def __str__(self):
        return chr(self.__symbol_dict[self.__char] + 0x2800)

    def __eq__(self, other):
        if isinstance(other, BrailleChar):
            return self.__char == other.__char
        raise TypeError("Can't compare these two types")

    def __ne__(self, other):
        return not self == other

    def get_points(self) -> tuple[bool, bool, bool, bool, bool, bool]:
        """Return a 6-tuple with bool values specifying which circles are black.

        :return: 6-tuple representing black circles
        """
        if self.__char == " ":
            return (
                False,
                False,
                False,
                False,
                False,
                False,
            )
        return tuple(
            ((self.__symbol_dict[self.__char] >> i) % 2 == 1 for i in range(6))
        )

    @classmethod
    def get_dict(cls):
        """Returns dictionary for translating from chars to unicode braille values.

        :return: Translation dictionary
        """
        return cls.__symbol_dict


class Braille:
    """Represents a string in braille.

    Can be subscripted, iterated through, compared for equality, added with other Braille objects,
    strings or BrailleChars. Can get its length by len function.
    """

    def __init__(self, characters: str | list[BrailleChar]):
        """Creates Braille object from characters.

        :param characters: String of alphabet and spaces
        """
        if isinstance(characters, str):
            correct = True
            for c in characters:
                correct = correct and (c.isalpha() or c == " ")
            if not correct:
                raise ValueError("All chars need to be alphabetical or a space")
            self.__seq = [BrailleChar(c) for c in characters.lower()]
        elif isinstance(characters, list):
            self.__seq = characters
        else:
            raise TypeError("Characters must be of type string")

    def __str__(self):
        return "".join(str(c) for c in self.__seq)

    def __eq__(self, other):
        if isinstance(other, Braille):
            return self.__seq == other.__seq
        raise TypeError("Can't compare these two types")

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.__seq)

    def __getitem__(self, item) -> BrailleChar:
        return self.__seq[item]

    def __add__(self, other):
        if isinstance(other, str):
            return Braille(self.__seq + [BrailleChar(c) for c in other])
        if isinstance(other, Braille):
            return Braille(self.__seq + other.__seq)
        if isinstance(other, BrailleChar):
            return Braille(self.__seq + [other])
        raise TypeError("Can't add these two types together")

    @staticmethod
    def get_dict():
        """Returns dictionary for translating from chars to unicode braille values.

        :return: Translation dictionary
        """
        return BrailleChar.get_dict()
