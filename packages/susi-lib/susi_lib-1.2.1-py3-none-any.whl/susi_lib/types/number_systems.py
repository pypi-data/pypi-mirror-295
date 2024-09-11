"""Provides NumberSystems class for representing strings as numbers."""


class NumberChar:
    """Represents a character as number."""

    __symbol_dict = {chr(ord("a") + x): x + 1 for x in range(26)}
    __format = {2: "05b", 10: "d", 16: "x"}

    def __init__(self, character, base=10):
        if not isinstance(character, str):
            raise TypeError
        if len(character) > 1 or (not character.isalpha() and character != " "):
            raise ValueError
        self.__char = character.lower()
        self.__base = base

    def change_base(self, base):
        """Changes the base used to convert the char to number.

        :param base: Int base of the desired system (2, 10, 16)
        """
        if not isinstance(base, int):
            raise TypeError
        self.__base = base

    def __str__(self):
        if self.__char == " ":
            return ""
        return format(self.__symbol_dict[self.__char], self.__format[self.__base])

    def __eq__(self, other):
        if not isinstance(other, NumberChar):
            raise TypeError("Can't compare these two types")
        return self.__char == other.__char and self.__base == other.__base

    def __ne__(self, other):
        return not self == other

    @classmethod
    def get_dict(cls):
        """Returns dictionary for translating from chars to base 10 ints.

        :return: Translation dictionary
        """
        return cls.__symbol_dict


class NumberSystems:
    """Represents a string as number.

    Can be subscripted, iterated through, compared for equality, added with other NumberSystems
    objects, strings or NumberChars. Can get its length by len function.
    """

    def __init__(self, characters: str | list[NumberChar], base=10):
        if not isinstance(base, int):
            raise TypeError("Base must an int")
        if base not in [2, 10, 16]:
            raise ValueError("Base must be 2, 10 or 16")
        if isinstance(characters, str):
            correct = True
            for c in characters.lower():
                correct = correct and (c.isalpha() or c == " ")
            if not correct:
                raise ValueError("All chars need to be alphabetical or a space")
            self.__base = base
            self.__seq = [NumberChar(c, self.__base) for c in characters.lower()]
        elif isinstance(characters, list):
            self.__base = base
            self.__seq = characters
        else:
            raise TypeError("Characters must be of type string")

    def __str__(self):
        return ", ".join(
            [str(c) for c in self.__seq if c != NumberChar(" ", self.__base)]
        )

    def __eq__(self, other):
        if isinstance(other, NumberSystems):
            return self.__seq == other.__seq and self.__base == other.__base
        raise TypeError("Can't compare these two types")

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.__seq)

    def __getitem__(self, item) -> NumberChar:
        return self.__seq[item]

    def __add__(self, other):
        if isinstance(other, str):
            return NumberSystems(
                self.__seq + [NumberChar(c, self.__base) for c in other]
            )
        if isinstance(other, NumberSystems):
            old_base = other.__base
            other.change_base(self.__base)
            ret = NumberSystems(self.__seq + other.__seq, self.__base)
            other.change_base(old_base)
            return ret
        if isinstance(other, NumberChar):
            return NumberSystems(self.__seq + [other], self.__base)
        raise TypeError("Can't add these two types")

    def change_base(self, base: int):
        """Changes the base used to convert the char to number.

        :param base: Int base of the desired system (2, 10, 16)
        """
        if not isinstance(base, int):
            raise TypeError("Base must an int")
        if base not in [2, 10, 16]:
            raise ValueError("Base must be 2, 10 or 16")
        self.__base = base
        for n in self.__seq:
            n.change_base(self.__base)

    @staticmethod
    def get_dict():
        """Returns dictionary for translating from chars to base 10 ints.

        :return: Translation dictionary
        """
        return NumberChar.get_dict()
