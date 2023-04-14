"""
Laboratorul de Criptografie și Protecția Datelor

@file lab3_1_1.py

@brief Laboratorul 3 - Exercițiul 1.1
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

KEY: str = 'CINESETREZESTEDEDIMINEATAAJUNGELADESTINATIE'
KEY = validate_text(KEY)

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'LABORATORULDECRIPTOGRAFIESIPROTECTIADATELOR'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We check if the length of the plaintext is equal to the length of the key
if len(PLAIN_TEXT) != len(KEY):
    raise ValueError(F'Textul de criptat are lungimea {len(PLAIN_TEXT)}, iar cheia are lungimea {len(KEY)}. Lungimile trebuie să fie egale!')

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26: Final[int] = 26

# We encrypt the plaintext
PLAIN_TEXT_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in PLAIN_TEXT)) - ASCII_OFFSET
KEY_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in KEY)) - ASCII_OFFSET
CRYPTED_TEXT_ARRAY: Final[ndarray] = (PLAIN_TEXT_ARRAY + KEY_ARRAY) % Z26
CRYPTED_TEXT: Final[str] = array_to_string((chr(char + ASCII_OFFSET) for char in CRYPTED_TEXT_ARRAY))

# We decrypt the encrypted text
DECRYPTED_TEXT_ARRAY: Final[ndarray] = (CRYPTED_TEXT_ARRAY + Z26 - KEY_ARRAY) % Z26
DECRYPTED_TEXT: Final[str] = array_to_string((chr(char + ASCII_OFFSET) for char in DECRYPTED_TEXT_ARRAY))

# We print the results
print(F'The encryption key is: {KEY}')
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
