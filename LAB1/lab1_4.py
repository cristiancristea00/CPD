"""
Laboratorul de Criptografie și Protecția Datelor

@file lab1_4.py

@brief Laboratorul 1 - Exercițiul 4
"""

from typing import Final, Iterable

import numpy as np
from numpy import ndarray
from sympy import Matrix
from tabulate import tabulate


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


def process_block(block: str, matrix: ndarray) -> str:
    """
    Encrypts or decrypts a block of text using the Hill cipher algorithm
    and using the given matrix.

    Args:
        block (str): The block of text to be encrypted/decrypted
        matrix (ndarray): The encryption/decryption matrix

    Returns:
        str: The encrypted/decrypted block
    """

    # We convert the block to an array of indices
    block_idx: Final[ndarray] = np.array(list(ord(char) for char in block)) - ASCII_OFFSET

    # We transform the block into a column matrix
    block_matrix: Final[ndarray] = block_idx.reshape((K_SIZE, 1))

    # We encrypt/decrypt the block
    cypher_idx: Final[ndarray] = ((matrix @ block_matrix) % Z26_NO).flatten()

    # We transform the indices into characters
    cypher_block = np.array(list(chr(idx + ASCII_OFFSET) for idx in cypher_idx))

    return array_to_string(cypher_block)


############################################
## Here you can change the encryption key ##
############################################

K_MATRIX: Final[ndarray] = np.array([[7, 20], [3, 5]])

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'LABORATORULDECRIPTOGRAFIE'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26_NO: Final[int] = 26

# We define the size of the encryption matrix
K_SIZE: Final[int] = K_MATRIX.shape[0]

# We check if the encryption matrix is invertible in Z26
try:

    K_INVERSE: Final[ndarray] = np.array(Matrix(K_MATRIX).inv_mod(Z26_NO))

except ValueError as exc:

    raise ValueError('Matricea K nu este inversabilă în Z26!') from exc

# We encrypt the plaintext
PADDED_TEXT: Final[str] = PLAIN_TEXT + 'Z' * (K_SIZE - len(PLAIN_TEXT) % K_SIZE)
SPLIT_TEXT: Final[ndarray] = np.array(list(PADDED_TEXT[i:i + K_SIZE] for i in range(0, len(PADDED_TEXT), K_SIZE)))
CYPHER_BLOCKS: Final[ndarray] = np.array(list(process_block(block, K_MATRIX) for block in SPLIT_TEXT))
PADDED_CRYPTED_TEXT: Final[str] = array_to_string(CYPHER_BLOCKS)
CRYPTED_TEXT: Final[str] = PADDED_CRYPTED_TEXT[0:len(PLAIN_TEXT)]

# We decrypt the encrypted text
SPLIT_DECRYPTED: Final[ndarray] = np.array(list(PADDED_CRYPTED_TEXT[i:i + K_SIZE] for i in range(0, len(PADDED_CRYPTED_TEXT), K_SIZE)))
DECRYPTED_BLOCKS: Final[ndarray] = np.array(list(process_block(block, K_INVERSE) for block in SPLIT_DECRYPTED))
DECRYPTED_TEXT: Final[str] = array_to_string(DECRYPTED_BLOCKS)[0:len(PLAIN_TEXT)]

# We print the results
print(F'The encryption matrix is:\n{tabulate(K_MATRIX, tablefmt="simple_grid")}')
print(F'The plain text is: {PLAIN_TEXT}')
print(F'The encrypted text is: {CRYPTED_TEXT}')
print(F'The decrypted text is: {DECRYPTED_TEXT}')
