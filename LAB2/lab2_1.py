"""
Laboratorul de Criptografie și Protecția Datelor

@file lab2_1.py

@brief Laboratorul 2 - Exercițiul 1
"""

from secrets import randbelow
from typing import Final, Iterable

import numpy as np
from numpy import ndarray


def validate_text(text: str) -> str:
    """
    Checks if the text contains only letters and converts it to
    uppercase.

    Args:
        text (str): The text to be validated

    Raises:
        ValueError: The text contains anything other than letters

    Returns:
        str: The uppercase text
    """

    allcaps = text.upper()
    result = ''.join(allcaps.split())

    if not result.isalpha():
        raise ValueError(F'The text {text} is NOT valid. It should contain only letters.')

    return result


def array_to_string(array: Iterable) -> str:
    """
    Converts an array to a string.

    Args:
        array (Iterable): The array

    Returns:
        str: The string
    """

    return ''.join(array)


############################################
## Here you can change the encryption key ##
############################################

PERM: Final[tuple] = (2, 6, 5, 3, 1, 4)

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'LABORATORULDECRIPTOGRAFIESIPROTECTIADATELOR'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We define the length of the key
KEY_LEN: Final[int] = len(PERM)

# We check if the permutation is valid
if sorted(PERM) != list(range(1, KEY_LEN + 1)):
    raise ValueError(F'Permutation {PERM} is not valid!')

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26: Final[int] = 26

# We pad the plaintext with random characters
REMAINDER: Final[int] = len(PLAIN_TEXT) % KEY_LEN
NO_CHARS_TO_ADD: Final[int] = KEY_LEN - REMAINDER if REMAINDER != 0 else 0
RANDOM_CHARS: Final[list] = [chr(randbelow(10 ** 10) % Z26 + ASCII_OFFSET) for _ in range(NO_CHARS_TO_ADD)]
PADDED_PLAIN_TEXT: Final[str] = PLAIN_TEXT + array_to_string(RANDOM_CHARS)

# We encrypt the plaintext
PLAIN_TEXT_ARRAY: Final[ndarray] = np.array(list(PADDED_PLAIN_TEXT))
PLAIN_TEXT_MATRIX: Final[ndarray] = PLAIN_TEXT_ARRAY.reshape(-1, KEY_LEN)
PERM_IDX: Final[ndarray] = np.array(PERM) - 1
CRYPTED_MATRIX: Final[ndarray] = PLAIN_TEXT_MATRIX[:, PERM_IDX]
CRYPTED_TEXT_ARRAY: Final[ndarray] = CRYPTED_MATRIX.flatten()
CRYPTED_TEXT: Final[str] = array_to_string(CRYPTED_TEXT_ARRAY)

# We decrypt the encrypted text
INV_PERM: Final[tuple] = tuple(np.argsort(PERM) + 1)
INV_PERM_IDX: Final[ndarray] = np.array(INV_PERM) - 1
DECRYPTED_MATRIX = CRYPTED_MATRIX[:, INV_PERM_IDX]
DECRYPTED_TEXT_ARRAY: Final[ndarray] = DECRYPTED_MATRIX.flatten()
DECRYPTED_TEXT: Final[str] = array_to_string(DECRYPTED_TEXT_ARRAY)[:len(PLAIN_TEXT)]

# We print the results
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The encryption permutation is: {PERM}')
print(F'The padded plain text is: {PADDED_PLAIN_TEXT}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decryption permutation is: {INV_PERM}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
