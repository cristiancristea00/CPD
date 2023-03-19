"""
Laboratorul de Criptografie și Protecția Datelor

@file compare.py

@brief Compararea frecvențelor de apariție a caracterelor
"""

import random
import re
from secrets import randbelow
from string import ascii_uppercase
from typing import Final, Iterable

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import seaborn as sns
from numpy import ndarray


# We set the seaborn theme and palette for the plots
sns.set_theme()
sns.set_palette("PuRd_r")


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


def create_graph(data: ndarray, title: str, axis: plt.Axes) -> None:
    """
    Plots the histogram of the data on the given axis.

    Args:
        data (ndarray): The data
        title (str): The title of the plot
        axis (plt.Axes): The axis on which the plot will be drawn
    """

    # Plot the histogram
    sns.histplot(data=data, bins=Z26_NO, stat='percent', discrete=True, shrink=0.9, linewidth=0, alpha=1, ax=axis)

    # Set the xticks to the letters of the alphabet
    axis.set_xticks(np.arange(Z26_NO))
    axis.set_xticklabels(ascii_uppercase)

    # Set the yticks to percentages
    axis.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

    # Set the title, x and y labels
    axis.set_title(title)
    axis.set_xlabel('Caractere')
    axis.set_ylabel('Frecvența')


# We read the text from the file
with open('LongText.txt', 'r', encoding='UTF-8') as file:
    TEXT = file.read()

# We remove all non-letter characters and convert the text to uppercase
TEXT = re.sub(R'[^a-zA-Z]', '', TEXT).upper()

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26_NO: Final[int] = 26

# We define the length of the text
TEXT_LEN: Final[int] = len(TEXT)


###################
## The plaintext ##
###################

TEXT_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in TEXT)) - ASCII_OFFSET


###################
## Caesar cipher ##
###################

### Here you can change the encryption key ###
CAESAR_KEY: Final[int] = 5

# We define the initial alphabet
CAESAR_ALPHA: Final[ndarray] = np.array(list(ascii_uppercase))

# We rotate the alphabet to the right by KEY positions
CAESAR_ROTATED_ALPHA: Final[ndarray] = np.roll(CAESAR_ALPHA, CAESAR_KEY)

# We encrypt the plaintext
CAESAR_IDX: Final[ndarray] = np.array([np.where(CAESAR_ALPHA == char) for char in TEXT]).flatten()
CAESAR_TEXT: Final[str] = CAESAR_ROTATED_ALPHA[CAESAR_IDX]
CAESAR_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in CAESAR_TEXT)) - ASCII_OFFSET


##########################
## Transposition cipher ##
##########################

### Here you can change the encryption key ###
TRANS_PERM: Final[tuple] = (2, 6, 5, 3, 1, 4)

# We define the length of the key
TRANS_KEY_LEN: Final[int] = len(TRANS_PERM)

# We check if the permutation is valid
if sorted(TRANS_PERM) != list(range(1, TRANS_KEY_LEN + 1)):
    raise ValueError(F'Permutarea {TRANS_PERM} nu este validă!')

# We pad the plaintext with random characters
TRANS_REMAINDER: Final[int] = len(TEXT) % TRANS_KEY_LEN
TRANS_NO_CHARS_TO_ADD: Final[int] = TRANS_KEY_LEN - TRANS_REMAINDER if TRANS_REMAINDER != 0 else 0
TRANS_RANDOM_CHARS: Final[list] = [chr(randbelow(10 ** 10) % Z26_NO + ASCII_OFFSET) for _ in range(TRANS_NO_CHARS_TO_ADD)]
TRANS_PADDED_PLAIN_TEXT: Final[str] = TEXT + array_to_string(TRANS_RANDOM_CHARS)

# We encrypt the plaintext
TRANS_PLAIN_TEXT_ARRAY: Final[ndarray] = np.array(list(TRANS_PADDED_PLAIN_TEXT))
TRANS_PLAIN_TEXT_MATRIX: Final[ndarray] = TRANS_PLAIN_TEXT_ARRAY.reshape(-1, TRANS_KEY_LEN)
TRANS_PERM_IDX: Final[ndarray] = np.array(TRANS_PERM) - 1
TRANS_CRYPTED_MATRIX = TRANS_PLAIN_TEXT_MATRIX[:, TRANS_PERM_IDX]
TRANS_ARRAY: Final[ndarray] = np.array([ord(char) for char in TRANS_CRYPTED_MATRIX.flatten()]) - ASCII_OFFSET


#####################
## Vigenère cipher ##
#####################

### Here you can change the encryption key ###
VIGINERE_KEY: str = 'CRIPTOGRAFIE'
VIGINERE_KEY = validate_text(VIGINERE_KEY)

# We make sure that the key is at least as long as the plaintext
VIGINERE_KEY += TEXT[:TEXT_LEN - len(VIGINERE_KEY)]

# We encrypt the plaintext
VIGINERE_KEY_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in VIGINERE_KEY)) - ASCII_OFFSET
VIGINERE_ARRAY: Final[ndarray] = (TEXT_ARRAY + VIGINERE_KEY_ARRAY) % Z26_NO


###################
## Vernam cipher ##
###################

# We encrypt the plaintext
random.seed(42)  # Folosim seed pentru a genera aceleași chei
VERNAM_ENCRYPTION_KEY_ARRAY: Final[ndarray] = np.array([random.randrange(0, Z26_NO) for _ in range(TEXT_LEN)])
VERNAM_ARRAY: Final[ndarray] = (TEXT_ARRAY + VERNAM_ENCRYPTION_KEY_ARRAY) % Z26_NO


############
## Graphs ##
############

# We create the figure and the corresponding axes
figure, axes = plt.subplots(2, 3, figsize=(20, 12))

# We set the figure spacing
figure.tight_layout(top=0.96, bottom=0.05, left=0.04, right=0.99, hspace=0.18, wspace=0.13)

# We create the graphs
create_graph(TEXT_ARRAY, 'Distribuția caracterelor din textul inițial', axes[0, 0])
create_graph(CAESAR_ARRAY, 'Distribuția caracterelor din textul cu substituție Cezar (monoalfabetică)', axes[0, 1])
create_graph(TRANS_ARRAY, 'Distribuția caracterelor din textul cu Transpoziție', axes[0, 2])
create_graph(VIGINERE_ARRAY, 'Distribuția caracterelor din textul cu substituție Vigenère (polialfabetică)', axes[1, 0])
create_graph(VERNAM_ARRAY, 'Distribuția caracterelor din textul criptat cu cifrul Vernam', axes[1, 1])

# We show the figure
plt.show()
