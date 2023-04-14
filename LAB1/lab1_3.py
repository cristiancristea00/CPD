"""
Laboratorul de Criptografie și Protecția Datelor

@file lab1_3.py

@brief Laboratorul 1 - Exercițiul 3
"""

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

A_COEF: Final[int] = 3
B_COEF: Final[int] = 5

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'LABORATORULDECRIPTOGRAFIE'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26_NO: Final[int] = 26

# We encrypt the plaintext
SPLIT_TEXT: Final[ndarray] = np.array(list(ord(char) for char in PLAIN_TEXT)) - ASCII_OFFSET  # Transformăm textul într-un array de valori ASCII
SPLIT_CYPHER: Final[ndarray] = (A_COEF * SPLIT_TEXT + B_COEF) % Z26_NO + ASCII_OFFSET
CRYPTED_TEXT: Final[str] = array_to_string(chr(char) for char in SPLIT_CYPHER)

# We decrypt the encrypted text
INV_COEF_A: Final[int] = pow(A_COEF, -1, Z26_NO)  # Calculăm inversul lui a în Z26
CYPHER_TEXT: Final[ndarray] = np.array(list(ord(char) for char in CRYPTED_TEXT)) - ASCII_OFFSET
SPLIT_DECRYPTED: Final[ndarray] = (INV_COEF_A * (CYPHER_TEXT - B_COEF)) % Z26_NO + ASCII_OFFSET
DECRYPTED_TEXT: Final[str] = array_to_string(chr(char) for char in SPLIT_DECRYPTED)

# We print the results
print(F"The affine encryption function's coefficients are: a = {A_COEF}, b = {B_COEF}")
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
