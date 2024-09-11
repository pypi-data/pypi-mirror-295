"""Provides Semaphore class for representing strings in semaphore encoding."""


class SemaphoreChar:
    """Represents a character in semaphore encoding."""

    __left = "\u2190"
    __up = "\u2191"
    __right = "\u2192"
    __down = "\u2193"
    __left_up = "\u2196"
    __right_up = "\u2197"
    __right_down = "\u2198"
    __left_down = "\u2199"
    __directions = [
        __down,
        __left_down,
        __left,
        __left_up,
        __up,
        __right_up,
        __right,
        __right_down,
    ]
    __symbol_dict = {
        "a": (2, 1),
        "b": (3, 1),
        "c": (4, 1),
        "d": (5, 1),
        "e": (1, 6),
        "f": (1, 7),
        "g": (1, 8),
        "h": (3, 2),
        "i": (4, 2),
        "j": (5, 7),
        "k": (2, 5),
        "l": (2, 6),
        "m": (2, 7),
        "n": (2, 8),
        "o": (3, 4),
        "p": (3, 5),
        "q": (3, 6),
        "r": (3, 7),
        "s": (3, 8),
        "t": (4, 5),
        "u": (4, 6),
        "v": (5, 6),
        "w": (6, 7),
        "x": (6, 8),
        "y": (4, 7),
        "z": (8, 7),
    }

    def __init__(self, character):
        if not isinstance(character, str):
            raise TypeError
        if len(character) > 1 or (not character.isalpha() and character != " "):
            raise ValueError
        self.__char = character.lower()

    def __str__(self):
        if self.__char == " ":
            return self.__char
        flag = self.__symbol_dict[self.__char]
        return (
            "(" + self.__directions[flag[0] - 1] + self.__directions[flag[1] - 1] + ")"
        )

    def __eq__(self, other):
        if isinstance(other, SemaphoreChar):
            return self.__char == other.__char
        raise TypeError("Can't compare these two types")

    def __ne__(self, other):
        return not self == other

    def get_directions(self) -> tuple[int, int]:
        """1-down, 2-down left, 3-left, 4-up left, 5-up, 6-up right, 7-right, 8-down right

        :return: Pair (1-8, 1-8) representing semaphore directions of the character
        """
        if self.__char == " ":
            return -1, -1
        return self.__symbol_dict[self.__char]

    @classmethod
    def get_dict(cls):
        """Returns dictionary for translating from chars to direction pairs.

        :return: Translation dictionary
        """
        return cls.__symbol_dict


class Semaphore:
    """Represents a string in semaphore.

    Can be subscripted, iterated through, compared for equality, added with other Semaphore
    objects, strings or SemaphoreChars. Can get its length by len function.
    """

    def __init__(self, characters: str | list[SemaphoreChar]):
        """Creates Semaphore object from characters.

        :param characters: String of alphabet and spaces
        """
        if isinstance(characters, str):
            correct = True
            for c in characters.lower():
                correct = correct and (c.isalpha() or c == " ")
            if not correct:
                raise ValueError("All chars need to be alphabetical or a space")
            self.__seq = [SemaphoreChar(c) for c in characters.lower()]
        elif isinstance(characters, list):
            self.__seq = characters
        else:
            raise TypeError("Characters must be of type string")

    def __str__(self):
        return "".join(str(c) for c in self.__seq)

    def __len__(self):
        return len(self.__seq)

    def __getitem__(self, item) -> SemaphoreChar:
        return self.__seq[item]

    def __add__(self, other):
        if isinstance(other, str):
            return Semaphore(self.__seq + [SemaphoreChar(c) for c in other])
        if isinstance(other, Semaphore):
            return Semaphore(self.__seq + other.__seq)
        if isinstance(other, SemaphoreChar):
            return Semaphore(self.__seq + [other])
        raise TypeError("Can't add these two types")

    def __eq__(self, other):
        if isinstance(other, Semaphore):
            return self.__seq == other.__seq
        raise TypeError("Can't compare these two types")

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def get_dict():
        """Returns dictionary for translating from chars to direction pairs.

        :return: Translation dictionary
        """
        return SemaphoreChar.get_dict()
