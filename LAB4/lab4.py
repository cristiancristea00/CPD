"""
Laboratorul de Criptografie și Protecția Datelor

@file lab4.py

@brief Laboratorul 4
"""

from pathlib import Path
from secrets import randbelow
from typing import Final

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import seaborn as sns
from numpy import ndarray
from skimage.io import imread

# We set the seaborn theme and palette for the plots
sns.set_theme()
sns.set_palette("PuRd_r")


def open_image(image_file: str) -> ndarray:
    """
    Opens an image.

    Args:
        image_file (str): The image file

    Returns:
        ndarray: The image
    """

    # We load the image as a float array
    image_path: Final[Path] = Path(__file__).resolve().parent / image_file
    float_image: Final[ndarray] = imread(image_path, as_gray=True)

    # We plot the original image
    axes_images[0, 0].imshow(np.uint8(np.round(float_image * 255)), cmap='gray')
    axes_images[0, 0].set_title('Original image')
    axes_images[0, 0].grid(False)

    # We plot the histogram of the original image
    create_histogram_graph(np.uint8(np.round(float_image * 255)), 'Original image', axes_histograms[0, 0])

    # We quantize the image to ZPIXEL values
    image: Final[ndarray] = np.uint8(np.round(float_image * (ZPIXEL - 1)))

    return image


def create_graph(image: ndarray, title: str, image_axis: plt.Axes, histogram_axis: plt.Axes) -> None:
    """
    Plots the image and the histogram of the image.

    Args:
        image (ndarray): The image
        title (str): The title of the plot
        image_axis (plt.Axes): The axis on which the image will be drawn
        histogram_axis (plt.Axes): The axis on which the histogram will be drawn
    """

    create_image_graph(image, title, image_axis)
    create_histogram_graph(image, title, histogram_axis)


def create_image_graph(image: ndarray, title: str, axis: plt.Axes) -> None:
    """
    Plots the image.

    Args:
        image (ndarray): The image
        title (str): The title of the plot
        axis (plt.Axes): The axis on which the plot will be drawn
    """

    # Plot the image
    axis.imshow(image * ZQUANTIZATION, cmap='gray')
    axis.grid(False)

    # Set the title
    axis.set_title(title)


def create_histogram_graph(data: ndarray, title: str, axis: plt.Axes) -> None:
    """
    Plots the histogram of the data on the given axis.

    Args:
        data (ndarray): The data
        title (str): The title of the plot
        axis (plt.Axes): The axis on which the plot will be drawn
    """

    # Plot the histogram
    sns.histplot(data=data.flatten(), bins=ZPIXEL, stat='percent', discrete=True, linewidth=0, alpha=1, ax=axis)

    # Set the yticks to percentages
    axis.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

    # Set the title, x and y labels
    axis.set_title(title)
    axis.set_ylabel('Frequency [%]')


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


### Here you can change the number of pixels ###
ZPIXEL: Final[int] = 32

# We define the quantization step
ZQUANTIZATION: Final[int] = 256 // ZPIXEL

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We create the figure for the images and the corresponding axes
figure_images, axes_images = plt.subplots(2, 3, figsize=(16, 10))

# We set the figure's spacing
figure_images.tight_layout(pad=3.0, w_pad=3.0, h_pad=3.0)

# We create the figure for the histograms and the corresponding axes
figure_histograms, axes_histograms = plt.subplots(2, 3, figsize=(16, 10))

# We set the figure's spacing
figure_histograms.tight_layout(pad=3.0, w_pad=3.0, h_pad=3.0)

#####################
## The plain image ##
#####################

IMAGE: Final[ndarray] = open_image('img.jpg')


###################
## Caesar cipher ##
###################

### Here you can change the encryption key ###
CAESAR_KEY: Final[int] = 20

# We encrypt the image
CAESAR_IMAGE: Final[ndarray] = (IMAGE + CAESAR_KEY) % ZPIXEL


##########################
## Transposition cipher ##
##########################

### Here you can change the encryption key ###
TRANS_PERM: Final[tuple] = (13, 8, 2, 14, 6, 11, 5, 3, 15, 9, 12, 1, 10, 4, 7)

# We define the length of the key
TRANS_KEY_LEN: Final[int] = len(TRANS_PERM)

# We check if the permutation is valid
if sorted(TRANS_PERM) != list(range(1, TRANS_KEY_LEN + 1)):
    raise ValueError(F'Permutation {TRANS_PERM} is not valid!')

# We pad the plaintext with random characters
TRANS_REMAINDER: Final[int] = IMAGE.size % TRANS_KEY_LEN
TRANS_NO_CHARS_TO_ADD: Final[int] = TRANS_KEY_LEN - TRANS_REMAINDER if TRANS_REMAINDER != 0 else 0
TRANS_RANDOM_CHARS: Final[list] = [randbelow(10 ** 10) % ZPIXEL for _ in range(TRANS_NO_CHARS_TO_ADD)]

# We encrypt the image
TRANS_IMAGE_ARRAY: Final[ndarray] = np.append(IMAGE.reshape(IMAGE.size), TRANS_RANDOM_CHARS)
TRANS_IMAGE_MATRIX: Final[ndarray] = TRANS_IMAGE_ARRAY.reshape(-1, TRANS_KEY_LEN)
TRANS_PERM_IDX: Final[ndarray] = np.array(TRANS_PERM) - 1
TRANS_CRYPTED_MATRIX: Final[ndarray] = TRANS_IMAGE_MATRIX[:, TRANS_PERM_IDX]
TRANS_CRYPTED_ARRAY: Final[ndarray] = TRANS_CRYPTED_MATRIX.reshape(TRANS_IMAGE_ARRAY.size)[:IMAGE.size]
TRANS_IMAGE: Final[ndarray] = TRANS_CRYPTED_ARRAY.reshape(IMAGE.shape)


#####################
## Vigenère cipher ##
#####################

### Here you can change the encryption key ###
VIGENERE_KEY: str = 'LABORATORULDECRIPTOGRAFIESIPROTECTIADATELOR'
VIGENERE_KEY = validate_text(VIGENERE_KEY)

# We make sure that the key is at least as long as the image
VIGENERE_KEY += (IMAGE.size // len(VIGENERE_KEY)) * VIGENERE_KEY
VIGENERE_KEY = VIGENERE_KEY[:IMAGE.size]

# We encrypt the plaintext
VIGENERE_KEY_ARRAY: Final[ndarray] = np.array(list(ord(char) for char in VIGENERE_KEY)) - ASCII_OFFSET
VIGENERE_KEY_MATRIX: Final[ndarray] = VIGENERE_KEY_ARRAY.reshape(IMAGE.shape)
VIGENERE_IMAGE: Final[ndarray] = (IMAGE + VIGENERE_KEY_MATRIX) % ZPIXEL


# We encrypt the plaintext
np.random.seed(42)  # We set the seed to make the encryption deterministic
VERNAM_KEY_MATRIX: Final[ndarray] = np.random.randint(0, ZPIXEL, IMAGE.shape)
VERNAM_IMAGE: Final[ndarray] = (IMAGE + VERNAM_KEY_MATRIX) % ZPIXEL


############
## Graphs ##
############

# We create the graphs
create_graph(IMAGE, 'Quantized image', axes_images[0, 1], axes_histograms[0, 1])
create_graph(CAESAR_IMAGE, 'Caesar cipher', axes_images[0, 2], axes_histograms[0, 2])
create_graph(TRANS_IMAGE, 'Transposition cipher', axes_images[1, 0], axes_histograms[1, 0])
create_graph(VIGENERE_IMAGE, 'Vigenère cipher', axes_images[1, 1], axes_histograms[1, 1])
create_graph(VERNAM_IMAGE, 'Vernam cipher', axes_images[1, 2], axes_histograms[1, 2])

# We show the figure
plt.show()
