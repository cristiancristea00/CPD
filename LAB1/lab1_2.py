"""
Laboratorul de Criptografie și Protecția Datelor

@file lab1_3.py

@brief Laboratorul 1 - Exercițiul 2
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


def array_to_string(array: Iterable[str]) -> str:
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

KEY: Final[str] = 'PAROLA'
KEY_SHIFT: Final[int] = 5

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: Final[str] = 'LABORATORULDECRIPTOGRAFIE'

# We define the initial alphabet
ALPHA: Final[ndarray] = np.array(list(ascii_uppercase))

# We build the cypher alphabet
CYPHER_ALPHA: ndarray = np.array(list(dict.fromkeys(KEY)))  # Remove duplicates

for char in ALPHA:
    if char not in CYPHER_ALPHA:
        CYPHER_ALPHA = np.append(CYPHER_ALPHA, char)

CYPHER_ALPHA = np.roll(CYPHER_ALPHA, KEY_SHIFT)

# We encrypt the plaintext
CRYPTED_IDX: Final[ndarray] = np.array([np.where(ALPHA == char) for char in PLAIN_TEXT]).flatten()
CRYPTED_TEXT: Final[str] = array_to_string(CYPHER_ALPHA[CRYPTED_IDX])

# We decrypt the encrypted text
DECRYPTED_IDX: Final[ndarray] = np.array([np.where(CYPHER_ALPHA == char) for char in CRYPTED_TEXT]).flatten()
DECRYPTED_TEXT: Final[str] = array_to_string(ALPHA[DECRYPTED_IDX])

# We print the results
print(F'The encryption key is: {KEY}')
print(F"The encryption key's shift is: {KEY_SHIFT}")
print(F'The initial alphabet is: {array_to_string(ALPHA)}')
print(F'The cypher alphabet is: {array_to_string(CYPHER_ALPHA)}')
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
