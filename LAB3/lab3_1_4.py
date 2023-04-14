"""
Laboratorul de Criptografie și Protecția Datelor

@file lab3_1_4.py

@brief Laboratorul 3 - Exercițiul 1.4
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

KEY: str = 'CRIPTOGRAFIE'
KEY = validate_text(KEY)

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'LABORATORULDECRIPTOGRAFIESIPROTECTIADATELOR'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We define the length of the key
KEY_LEN: Final[int] = len(KEY)

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26_NO: Final[int] = 26

# We pad the plaintext with random characters
REMAINDER: Final[int] = len(PLAIN_TEXT) % KEY_LEN
NO_CHARS_TO_ADD: Final[int] = KEY_LEN - REMAINDER if REMAINDER != 0 else 0
RANDOM_CHARS: Final[list] = [chr(randbelow(10 ** 10) % Z26_NO + ASCII_OFFSET) for _ in range(NO_CHARS_TO_ADD)]
PADDED_PLAIN_TEXT: Final[str] = PLAIN_TEXT + array_to_string(RANDOM_CHARS)

# We encrypt the plaintext
print('ENCRYPTING THE PLAINTEXT:', end='\n' * 2)

CURRENT_KEY: str = KEY
CRYPTED_TEXT: str = ''

for idx in range(len(PADDED_PLAIN_TEXT) // KEY_LEN):
    print(F'Iteration {idx + 1}:')
    print('-' * KEY_LEN * 4)

    CURRENT_TEXT: str = PADDED_PLAIN_TEXT[idx * KEY_LEN:(idx + 1) * KEY_LEN]
    print(F'The plaintext is: {CURRENT_TEXT}')

    print(F'Curent key is: {CURRENT_KEY}')

    PLAIN_TEXT_ARRAY: ndarray = np.array(list(ord(char) for char in CURRENT_TEXT)) - ASCII_OFFSET
    KEY_ARRAY: ndarray = np.array(list(ord(char) for char in CURRENT_KEY)) - ASCII_OFFSET
    CRYPTED_TEXT_ARRAY: ndarray = (PLAIN_TEXT_ARRAY + KEY_ARRAY) % Z26_NO
    CRYPTED_STRING: str = array_to_string((chr(char + ASCII_OFFSET) for char in CRYPTED_TEXT_ARRAY))
    CRYPTED_TEXT += CRYPTED_STRING
    CURRENT_KEY = CRYPTED_STRING

    print(F'The encrypted text is: {CRYPTED_STRING}')
    print('-' * KEY_LEN * 4, end='\n' * 2)

print(end='\n' * 2)

# We decrypt the encrypted text
print('DECRYPTING THE ENCRYPTED TEXT:', end='\n' * 2)

CURRENT_KEY = KEY
DECRYPTED_TEXT: str = ''

for idx in range(len(CRYPTED_TEXT) // KEY_LEN):
    print(F'Iteration {idx + 1}:')
    print('-' * KEY_LEN * 4)

    CURRENT_CRYPTED_TEXT: str = CRYPTED_TEXT[idx * KEY_LEN:(idx + 1) * KEY_LEN]
    print(F'The encrypted text is: {CURRENT_CRYPTED_TEXT}')

    print(F'Curent key is: {CURRENT_KEY}')

    CURRENT_CRYPTED_ARRAY: ndarray = np.array(list(ord(char) for char in CURRENT_CRYPTED_TEXT)) - ASCII_OFFSET
    DECRYPT_KEY_ARRAY: ndarray = np.array(list(ord(char) for char in CURRENT_KEY)) - ASCII_OFFSET
    DECRYPTED_TEXT_ARRAY: ndarray = (CURRENT_CRYPTED_ARRAY - DECRYPT_KEY_ARRAY) % Z26_NO
    DECRYPTED_STRING: str = array_to_string((chr(char + ASCII_OFFSET) for char in DECRYPTED_TEXT_ARRAY))
    DECRYPTED_TEXT += DECRYPTED_STRING
    CURRENT_KEY = CURRENT_CRYPTED_TEXT

    print(F'The decrypted text is: {DECRYPTED_STRING}')
    print('-' * KEY_LEN * 4, end='\n' * 2)

DECRYPTED_TEXT = DECRYPTED_TEXT[:len(PLAIN_TEXT)]

print(end='\n' * 2)

# We print the results
print(F'The encryption key is: {KEY}')
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The padded plain text is: {PADDED_PLAIN_TEXT}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
