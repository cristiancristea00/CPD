"""
Laboratorul de Criptografie și Protecția Datelor

@file lab1_1.py

@brief Laboratorul 1 - Exercițiul 1
"""

from string import ascii_uppercase
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

KEY: Final[int] = 5

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'VIATALATARA'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We define the initial alphabet
ALPHA: Final[ndarray] = np.array(list(ascii_uppercase))

# We rotate the alphabet to the right by KEY positions
ROTATED_ALPHA: Final[ndarray] = np.roll(ALPHA, KEY)

# We encrypt the plaintext
CRYPTED_IDX: Final[ndarray] = np.array([np.where(ALPHA == char) for char in PLAIN_TEXT]).flatten()
CRYPTED_TEXT: Final[str] = array_to_string(ROTATED_ALPHA[CRYPTED_IDX])

# We decrypt the encrypted text
DECRYPTED_IDX: Final[ndarray] = np.array([np.where(ROTATED_ALPHA == char) for char in CRYPTED_TEXT]).flatten()
DECRYPTED_TEXT: Final[str] = array_to_string(ALPHA[DECRYPTED_IDX])

# We print the results
print(F'The encryption key is: {KEY}')
print(F'The initial alphabet is: {array_to_string(ALPHA)}')
print(F'The {KEY}-right rotated alphabet is: {array_to_string(ROTATED_ALPHA)}')
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
