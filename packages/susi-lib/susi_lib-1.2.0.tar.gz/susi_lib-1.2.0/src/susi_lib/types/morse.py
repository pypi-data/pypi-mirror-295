"""Provides Morse class for representing a string in morse encoding."""

from typing import List, Union


class Morse:
    """Represents a string in morse.

    Can be subscripted, iterated through, compared for equality, added with other Morse objects,
    strings.. Can get its length by len function.
    """

    def __init__(self, data: Union[str, "MorseSymbol", "MorseSequence"]):
        if isinstance(data, str):
            self.__data = MorseSymbol(data) if len(data) < 2 else MorseSequence(data)
            self.dots = self.__data.dots
            self.dashes = self.__data.dashes
        elif not isinstance(data, MorseSymbol) and not isinstance(data, MorseSequence):
            raise TypeError("Data must be a string")
        else:
            self.__data = data
            self.dots = self.__data.dots
            self.dashes = self.__data.dashes

    def __eq__(self, other):
        if not isinstance(other, Morse):
            raise TypeError("Can't compare these two types")
        return self.__data == other.__data

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.__data)

    def __add__(self, other):
        if isinstance(other, str):
            other = Morse(other)
        if not isinstance(other, Morse):
            raise TypeError("Can't add these two types")
        return Morse(self.__data + other.__data)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, item):
        return self.__data[item]

    def get(self):
        """

        :return: Underlying sequence of MorseSymbols
        """
        return self.__data.get()

    @staticmethod
    def get_dict():
        """Returns dictionary for translating from chars to morse.

        :return: Translation dictionary
        """
        return MorseSymbol.get_dict()


class MorseSymbol:
    """Represents a single morse character."""

    __dot = "."
    __dash = "-"
    __symbol_separator = "/"
    __word_separator = "⫽"
    __symbol_dict = {
        "a": __dot + __dash,
        "b": __dash + __dot + __dot + __dot,
        "c": __dash + __dot + __dash + __dot,
        "d": __dash + __dot + __dot,
        "e": __dot,
        "f": __dot + __dot + __dash + __dot,
        "g": __dash + __dash + __dot,
        "h": __dot + __dot + __dot + __dot,
        "i": __dot + __dot,
        "j": __dot + __dash + __dash + __dash,
        "k": __dash + __dot + __dash,
        "l": __dot + __dash + __dot + __dot,
        "m": __dash + __dash,
        "n": __dash + __dot,
        "o": __dash + __dash + __dash,
        "p": __dot + __dash + __dash + __dot,
        "q": __dash + __dash + __dot + __dash,
        "r": __dot + __dash + __dot,
        "s": __dot + __dot + __dot,
        "t": __dash,
        "u": __dot + __dot + __dash,
        "v": __dot + __dot + __dot + __dash,
        "w": __dot + __dash + __dash,
        "x": __dash + __dot + __dot + __dash,
        "y": __dash + __dot + __dash + __dash,
        "z": __dash + __dash + __dot + __dot,
        " ": __word_separator,
        "": __symbol_separator,
    }
    __symbol_dict_rev = {(v, k) for k, v in __symbol_dict.items()}

    def __init__(self, character: str):
        if not character.isalpha() and character != " " and character != "":
            raise ValueError("Character is not part of alphabet")
        if len(character) > 1:
            raise ValueError("Character is too long")
        self.__character = character.lower()
        self.dots = self.__symbol_dict[self.__character].count(self.__dot)
        self.dashes = self.__symbol_dict[self.__character].count(self.__dash)

    def __str__(self):
        return self.__symbol_dict[self.__character]

    def __eq__(self, other):
        if isinstance(other, MorseSymbol):
            return self.__character == other.__character
        raise TypeError("Can't compare these two types")

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        if self.__character in {"", " "}:
            return other
        if isinstance(other, MorseSymbol):
            if other.__character not in {" ", ""}:
                return MorseSequence(init=[self, MorseSymbol(""), other])
            return MorseSequence(init=[self, other])
        if isinstance(other, MorseSequence):
            return (self + MorseSymbol("")) + other
        raise TypeError("Can't add these types")

    def __len__(self):
        if self.__character in {"", " "}:
            return 0
        return len(self.__symbol_dict[self.__character])

    def get(self):
        """

        :return: Underlying sequence of MorseSymbols
        """
        return [self]

    def __getitem__(self, item):
        if item != 0:
            raise IndexError("Only valid index is 0")
        return self

    @classmethod
    def get_dict(cls):
        """Returns dictionary for translating from chars to morse.

        :return: Translation dictionary
        """
        return cls.__symbol_dict


class MorseSequence:
    """Represents a sequence of morse characters."""

    def __init__(self, text="", init=None):
        if init is None:
            init = []
        if isinstance(text, str):
            correct = True
            for c in text.lower():
                correct = correct and (c.isalpha() or c == " " or c == "")
            if not correct:
                raise ValueError("All chars need to be alphabetical or a space")
        self.__seq: List[MorseSymbol] = []
        if len(text) != 0:
            first = True
            for c in text.lower():
                if first and c == " ":
                    continue
                if first and c != " ":
                    self.__seq.append(MorseSymbol(c))
                    first = False
                    continue
                if (
                    not first
                    and c != " "
                    and self.__seq[-1] not in (MorseSymbol(" "), MorseSymbol(""))
                ):
                    self.__seq.append(MorseSymbol(""))
                if c != " " or self.__seq[-1] not in (
                    MorseSymbol(" "),
                    MorseSymbol(""),
                ):
                    self.__seq.append(MorseSymbol(c))
            self.dots = sum((x.dots for x in self.__seq))
            self.dashes = sum((x.dashes for x in self.__seq))
            return
        self.__seq = init
        self.dots = sum((x.dots for x in self.__seq))
        self.dashes = sum((x.dashes for x in self.__seq))

    def __str__(self):
        return "".join([str(x) for x in self.__seq])

    def __add__(self, other: Union["MorseSequence", MorseSymbol]):
        if isinstance(other, MorseSequence):
            if self.__seq[-1] not in (MorseSymbol(" "), MorseSymbol("")):
                self.__seq += MorseSymbol("") + other.__seq
            else:
                self.__seq += other.__seq
            return self

        if isinstance(other, MorseSymbol):
            if self.__seq[-1] not in (MorseSymbol(" "), MorseSymbol("")):
                self.__seq += [MorseSymbol(""), other]
            else:
                self.__seq.append(other)
            return self
        raise TypeError("Can't add these types")

    def __eq__(self, other):
        if not isinstance(other, MorseSequence):
            raise TypeError("Can't compare these two types")
        for left, right in zip(self.__seq, other.__seq):
            if left != right:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return sum(
            (
                1 if m not in (MorseSymbol(""), MorseSymbol(" ")) else 0
                for m in self.__seq
            )
        )

    def __getitem__(self, item):
        return self.__seq[item]

    def get(self):
        """

        :return: Underlying sequence of MorseSymbols
        """
        return self.__seq
