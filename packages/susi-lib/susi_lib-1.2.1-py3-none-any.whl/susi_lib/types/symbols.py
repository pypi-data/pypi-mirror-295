"""Provides Symbols class for easy converting between encodings of one string."""

from susi_lib.types.braille import Braille
from susi_lib.types.morse import Morse
from susi_lib.types.number_systems import NumberSystems
from susi_lib.types.semaphore import Semaphore


class Symbols:
    """Class for storing a string and getting its encodings.

    Can be subscripted, iterated through, compared for equality, added with other Symbols objects
    or strings. Can get its length by len function.
    Provides functions to get other encodings.
    """

    __rev_braille = {
        chr(value + 0x2800): key for key, value in Braille.get_dict().items()
    }

    __rev_semaphore = {
        "↙↓": "a",
        "←↓": "b",
        "↖↓": "c",
        "↑↓": "d",
        "↓↗": "e",
        "↓→": "f",
        "↓↘": "g",
        "←↙": "h",
        "↖↙": "i",
        "↑→": "j",
        "↙↑": "k",
        "↙↗": "l",
        "↙→": "m",
        "↙↘": "n",
        "←↖": "o",
        "←↑": "p",
        "←↗": "q",
        "←→": "r",
        "←↘": "s",
        "↖↑": "t",
        "↖↗": "u",
        "↑↗": "v",
        "↗→": "w",
        "↗↘": "x",
        "↖→": "y",
        "↘→": "z",
    }

    __dot = "."
    __dash = "-"
    __symbol_separator = "/"
    __word_separator = "⫽"
    __rev_morse = {value: key for key, value in Morse.get_dict().items()}

    def __init__(self, characters: str):
        """Creates Symbols from characters.

        :param characters: String to store
        """
        if not isinstance(characters, str):
            raise TypeError("Characters must be of type string")
        self.__characters = characters.lower()

    @classmethod
    def from_string(cls, string: str) -> str:
        """Decodes a string in either braille, morse, numbers or semaphore encoding.

        :param string: String to decode
        :return: Decoded string
        """
        if not isinstance(string, str):
            raise TypeError("String needs to be a string")
        r = cls.__braille_from_string(string)
        if r[0]:
            return r[1].strip()
        r = cls.__semaphore_from_string(string)
        if r[0]:
            return r[1].strip()
        r = cls.__numbers_from_string(string)
        if r[0]:
            return r[1].strip()
        r = cls.__morse_from_string(string)
        if r[0]:
            return r[1].strip()
        raise ValueError("Can't decode this string")

    @classmethod
    def __braille_from_string(cls, string: str):
        result = ""
        for c in string:
            if c not in cls.__rev_braille.keys():
                return False, ""
            result += cls.__rev_braille[c]
        return True, result

    @classmethod
    def __semaphore_from_string(cls, string: str):
        result = ""
        for word in string.split(" "):
            if len(word) % 4 != 0:
                return False, ""
            for i in range(len(word) // 4):
                begin = i * 4
                if word[begin] != "(" or word[begin + 3] != ")":
                    return False, ""
                if word[begin + 1 : begin + 3] not in cls.__rev_semaphore:
                    return False, ""
                result += cls.__rev_semaphore[word[begin + 1 : begin + 3]]
            result += " "
        return True, result

    @classmethod
    def __morse_from_string(cls, string: str):
        result = ""
        for word in string.split(cls.__word_separator):
            for char in word.split(cls.__symbol_separator):
                if char not in cls.__rev_morse.keys():
                    return False, ""
                result += cls.__rev_morse[char]
            result += " "
        return True, result

    @classmethod
    def __numbers_from_string(cls, string: str):
        nums = string.split(", ")
        bases = [2, 10, 16]
        base = 2
        miss = 0
        for b in bases:
            try:
                int(nums[0], b)
            except ValueError:
                miss += 1
            else:
                base = b
                break
        if miss == 3:
            return False, ""
        result = ""
        for num in nums:
            result += chr(ord("a") - 1 + int(num, base))
        return True, result

    def to_braille(self) -> Braille:
        """

        :return: Braille representation
        """
        return Braille(self.__characters)

    def to_morse(self) -> Morse:
        """

        :return: Morse representation
        """
        return Morse(self.__characters)

    def to_number_systems(self, base=10) -> NumberSystems:
        """

        :param base: Int base of the desired system (2, 10, 16)
        :return: Numbers representation
        """
        if not isinstance(base, int):
            raise TypeError("Base must an int")
        if base not in [2, 10, 16]:
            raise ValueError("Base must be 2, 10 or 16")
        return NumberSystems(self.__characters, base)

    def to_semaphore(self) -> Semaphore:
        """

        :return: Semaphore representation
        """
        return Semaphore(self.__characters)

    def __getitem__(self, item) -> "Symbols":
        return Symbols(self.__characters[item])

    def __str__(self):
        return self.__characters

    def __len__(self):
        return len(self.__characters)

    def __eq__(self, other):
        if not isinstance(other, Symbols):
            raise TypeError("Can't compare these two types")
        return self.__characters == other.__characters

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if isinstance(other, str):
            return Symbols(self.__characters + other)
        if isinstance(other, Symbols):
            return Symbols(self.__characters + other.__characters)
        raise TypeError("Can't add these two types")
