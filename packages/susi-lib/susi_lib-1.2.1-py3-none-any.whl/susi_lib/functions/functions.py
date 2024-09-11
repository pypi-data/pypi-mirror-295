"""Contains some useful functions"""

from enum import Enum, auto

from susi_lib.types import Symbols


def is_palindrome(word):
    """Checks if a value is a palindrome (is the same from front and back).

    :param word: value to check, it needs to have __getitem__, __len__ and __ne__
    :return: True if it is a palindrome, False when it is not
    """
    for i in range(len(word) // 2):
        if word[i] != word[-(i + 1)]:
            return False
    return True


def decode(string: str):
    """Decodes a given value.

    Supported encodings are Braille, Numbers, Morse and Semaphore. Encoding should be the same
    as the strings returned by __str__ method of classes in susi_lib.types.
    :param string: The string to decode
    :return: Decoded string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return Symbols.from_string(string)


def _encode_morse(string: str):
    """Encode the given string into morse.

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :return: Encoded morse string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return str(Symbols(string).to_morse())


def _encode_braille(string: str):
    """Encode the given string into braille.

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :return: Encoded braille string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return str(Symbols(string).to_braille())


def _encode_semaphore(string: str):
    """Encode the given string into semaphore.

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :return: Encoded semaphore string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    return str(Symbols(string).to_semaphore())


def _encode_numbers(string: str, base=10):
    """Encode the given string into numbers of given base

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :param base: The base of the number system (2, 10, 16)
    :return: Encoded numbers string
    """
    if not isinstance(string, str):
        raise TypeError("String needs to be a string")
    if not isinstance(base, int):
        raise TypeError("Base must be an int")
    if base not in [2, 10, 16]:
        raise ValueError("Valid values for base are 2, 10, 16")
    return str(Symbols(string).to_number_systems(base))


class Encoding(Enum):
    MORSE = auto()
    BRAILLE = auto()
    SEMAPHORE = auto()
    NUMBERS = auto()


def encode(string: str, encoding: Encoding, base: int = 10):
    """Encode the given string into desired encoding

    :param string: The string to encode (should contain only alphabetical chars and spaces)
    :param encoding: Desired encoding, MORSE, BRAILLE, SEMAPHORE, NUMBERS
    :param base: The base of the number system (2, 10, 16), needed only for NUMBERS
    :return: Encoded string
    """
    match (encoding):
        case Encoding.MORSE:
            return _encode_morse(string)
        case Encoding.BRAILLE:
            return _encode_braille(string)
        case Encoding.SEMAPHORE:
            return _encode_semaphore(string)
        case Encoding.NUMBERS:
            return _encode_numbers(string, base)
        case _:
            raise ValueError("Invalid enum value")


def _calculate_freq(word: str):
    word_freq = {}
    for c in word:
        word_freq[c] = word_freq.get(c, 0) + 1
    return word_freq


def find_anagrams(word: str, word_list: list[str]):
    if not isinstance(word, str):
        raise TypeError("Word must be a string")
    if not isinstance(word_list, list):
        raise TypeError("Word_list must be a list")
    if not all(isinstance(val, str) for val in word_list):
        raise TypeError("Word_list must be a list of strings")
    filtered_words = [w for w in word_list if len(w) == len(word) and w != word]
    word_freq = _calculate_freq(word)
    found_words: list[str] = []

    for w in filtered_words:
        if word_freq == _calculate_freq(w):
            found_words.append(w)

    return found_words
