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


def create_graph(data: ndarray, title: str, axis: plt.Axes) -> None:
    """
    Plots the histogram of the data on the given axis.

    Args:
        data (ndarray): The data
        title (str): The title of the plot
        axis (plt.Axes): The axis on which the plot will be drawn
    """

    # Plot the histogram
    sns.histplot(data=data, bins=Z26, stat='percent', discrete=True, shrink=0.9, linewidth=0, alpha=1, ax=axis)

    # Set the xticks to the letters of the alphabet
    axis.set_xticks(np.arange(Z26))
    axis.set_xticklabels(ascii_uppercase)

    # Set the yticks to percentages
    axis.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

    # Set the title, x and y labels
    axis.set_title(title)
    axis.set_ylabel('Frequency [%]')


# We read the text from the file
with open('LongText.txt', 'r', encoding='UTF-8') as file:
    TEXT = file.read()

# We remove all non-letter characters and convert the text to uppercase
TEXT = re.sub(R'[^a-zA-Z]', '', TEXT).upper()

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We define the number of letters in the alphabet
Z26: Final[int] = 26

# We define the length of the text
TEXT_LEN: Final[int] = len(TEXT)

# We create the figure and the corresponding axes
figure, axes = plt.subplots(2, 3, figsize=(16, 10))

# We set the figure's spacing
figure.tight_layout(pad=3.0, w_pad=3.0, h_pad=3.0)

# We disable the last axis
axes[1, 2].axis('off')


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
    raise ValueError(F'Permutation {TRANS_PERM} is not valid!')

# We pad the plaintext with random characters
TRANS_REMAINDER: Final[int] = len(TEXT) % TRANS_KEY_LEN
TRANS_NO_CHARS_TO_ADD: Final[int] = TRANS_KEY_LEN - TRANS_REMAINDER if TRANS_REMAINDER != 0 else 0
TRANS_RANDOM_CHARS: Final[list] = [chr(randbelow(10 ** 10) % Z26 + ASCII_OFFSET) for _ in range(TRANS_NO_CHARS_TO_ADD)]
TRANS_PADDED_PLAIN_TEXT: Final[str] = TEXT + array_to_string(TRANS_RANDOM_CHARS)

# We encrypt the plaintext
TRANS_PLAIN_TEXT_ARRAY: Final[ndarray] = np.array(list(TRANS_PADDED_PLAIN_TEXT))
TRANS_PLAIN_TEXT_MATRIX: Final[ndarray] = TRANS_PLAIN_TEXT_ARRAY.reshape(-1, TRANS_KEY_LEN)
TRANS_PERM_IDX: Final[ndarray] = np.array(TRANS_PERM) - 1
TRANS_CRYPTED_MATRIX: Final[ndarray] = TRANS_PLAIN_TEXT_MATRIX[:, TRANS_PERM_IDX]
TRANS_ARRAY: Final[ndarray] = np.array([ord(char) for char in TRANS_CRYPTED_MATRIX.flatten()]) - ASCII_OFFSET


#####################
## Vigenère cipher ##
#####################

### Here you can change the encryption key ###
VIGENERE_KEY: str = 'CRIPTOGRAFIE'
VIGENERE_KEY = validate_text(VIGENERE_KEY)

# We make sure that the key is at least as long as the plaintext
VIGENERE_KEY += TEXT[:TEXT_LEN - len(VIGENERE_KEY)]

# We encrypt the plaintext
VIGENERE_KEY_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in VIGENERE_KEY)) - ASCII_OFFSET
VIGENERE_ARRAY: Final[ndarray] = (TEXT_ARRAY + VIGENERE_KEY_ARRAY) % Z26


###################
## Vernam cipher ##
###################

# We encrypt the plaintext
random.seed(42)  # We set the seed to make the encryption deterministic
VERNAM_ENCRYPTION_KEY_ARRAY: Final[ndarray] = np.array([random.randrange(0, Z26) for _ in range(TEXT_LEN)])
VERNAM_ARRAY: Final[ndarray] = (TEXT_ARRAY + VERNAM_ENCRYPTION_KEY_ARRAY) % Z26


############
## Graphs ##
############

# We create the graphs
create_graph(TEXT_ARRAY, 'Initial plaintext', axes[0, 0])
create_graph(CAESAR_ARRAY, 'Caesar cipher (monoalpabetic substitution)', axes[0, 1])
create_graph(TRANS_ARRAY, 'Transposition cipher (permutation)', axes[0, 2])
create_graph(VIGENERE_ARRAY, 'Vigenère cipher (polyalphabetic substitution)', axes[1, 0])
create_graph(VERNAM_ARRAY, 'Vernam cipher (one-time pad)', axes[1, 1])

# We show the figure
plt.show()
