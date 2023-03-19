"""
Laboratorul de Criptografie și Protecția Datelor

@file lab3_2.py

@brief Laboratorul 3 - Exercițiul 2
"""

import random
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

    if not text.isalpha():
        raise ValueError(F'Textul "{text}" nu este valid! Textul trebuie să conțină doar litere!')

    return text.upper()


def array_to_string(array: Iterable) -> str:
    """
    Converts an array to a string.

    Args:
        array (Iterable): The array

    Returns:
        str: The string
    """

    return ''.join(array)


#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'LABORATORULDECRIPTOGRAFIESIPROTECTIADATELOR'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26_NO: Final[int] = 26

# We encrypt the plaintext
random.seed(42) # We use a seed to generate the same keys
ENCRYPTION_KEY_CHARS: list = (chr(random.randrange(0, Z26_NO) + ASCII_OFFSET) for _ in range(len(PLAIN_TEXT)))
ENCRYPTION_KEY: str = array_to_string(ENCRYPTION_KEY_CHARS)
PLAIN_TEXT_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in PLAIN_TEXT)) - ASCII_OFFSET
ENCRYPTION_KEY_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in ENCRYPTION_KEY)) - ASCII_OFFSET
CRYPTED_TEXT_ARRAY: Final[ndarray] = (PLAIN_TEXT_ARRAY + ENCRYPTION_KEY_ARRAY) % Z26_NO
CRYPTED_TEXT: Final[str] = array_to_string((chr(char + ASCII_OFFSET) for char in CRYPTED_TEXT_ARRAY))

# We decrypt the encrypted text
random.seed(42) # We use a seed to generate the same keys
DECRYPTION_KEY_CHARS: list = (chr(random.randrange(0, Z26_NO) + ASCII_OFFSET) for _ in range(len(PLAIN_TEXT)))
DECRYPTION_KEY: str = array_to_string(DECRYPTION_KEY_CHARS)
DECRYPTION_KEY_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in DECRYPTION_KEY)) - ASCII_OFFSET
DECRYPTED_TEXT_ARRAY: Final[ndarray] = (CRYPTED_TEXT_ARRAY + Z26_NO - DECRYPTION_KEY_ARRAY) % Z26_NO
DECRYPTED_TEXT: Final[str] = array_to_string((chr(char + ASCII_OFFSET) for char in DECRYPTED_TEXT_ARRAY))

# We print the results
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The encryption key is: {ENCRYPTION_KEY}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decryption key is: {DECRYPTION_KEY}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
