"""
Laboratorul de Criptografie și Protecția Datelor

@file lab5.py

@brief Laboratorul 5
"""

from itertools import chain
from textwrap import wrap
from typing import Final, Iterable


def validate_text(text: str) -> str:
    """
    Checks if the text contains only letters and converts it to
    uppercase. If the number of characters is odd, it adds a space.

    Args:
        text (str): The text to be validated

    Raises:
        ValueError: The text contains anything other than letters and spaces

    Returns:
        str: The uppercase text
    """

    result = text.upper()

    if not result.replace(' ', '').isalpha():
        raise ValueError(F'The text {text} is NOT valid. It should contain only letters and spaces.')

    if len(result) % 2 != 0:
        result += ' '

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


def character_map(character: str) -> int:
    """
    Maps a character to a number.

    Args:
        character (str): The character

    Returns:
        int: The number
    """

    if character == ' ':
        return 26

    return ord(character) - ASCII_OFFSET


def inverse_character_map(number: int) -> str:
    """
    Maps a number to a character.

    Args:
        number (int): The number

    Returns:
        str: The character
    """

    if number == 26:
        return ' '

    return chr(number + ASCII_OFFSET)


def euclid(modulus: int, prime: int) -> int:
    """
    Extended Euclid algorithm.

    Args:
        modulus (int): The modulus number
        prime (int): The prime number

    Returns:
        int: The inverse of the prime number modulo the modulus number
    """

    return pow(prime, -1, modulus)


def knapsack(public_key: tuple, value: int) -> str:
    """
    Knapsack algorithm.

    Args:
        public_key (tuple): The public key
        value (int): The value

    Returns:
        str: The binary representation of the value
    """

    binary: Final[list[str]] = []

    for key in reversed(public_key):
        if value >= key:
            value -= key
            binary.append('1')
        else:
            binary.append('0')

    result: Final[str] = array_to_string(reversed(binary))

    return result


def generate_public_key(private_key: tuple, modulus: int, prime: int) -> tuple:
    """
    Generates a public key from a private key.

    Args:
        private_key (tuple): The private key
        modulus (int): The modulus number
        prime (int): The prime number

    Returns:
        tuple: The public key
    """

    public_key: Iterable[int] = (key * prime % modulus for key in private_key)

    return tuple(public_key)


def encrypt(message: str, public_key: tuple) -> tuple:
    """
    Encrypts a message using a public key.

    Args:
        message (str): The message
        public_key (tuple): The public key

    Returns:
        tuple: The encrypted message
    """

    # We convert the message to a list of indices
    indices: Final[Iterable[int]] = (character_map(char) for char in message)

    # We convert the indices to binary
    binary: Final[Iterable[str]] = (F'{elem:05b}' for elem in indices)

    # We concatenate the binary numbers
    concatenated: Final[str] = array_to_string(binary)

    # We divide the concatenated binary number into chunks of 10
    divided: Final[list[str]] = wrap(concatenated, 10)

    cryptogram: Final[list[int]] = []

    for elem in divided:
        # We convert the bits to integers
        bits: Iterable[int] = (int(bit) for bit in elem)

        # We multiply each bit with the corresponding key and sum them
        pairs: Iterable[tuple[int, int]] = zip(bits, public_key)
        current_crypted: int = sum(bit * key for bit, key in pairs)

        # We add the current encrypted number to the cryptogram
        cryptogram.append(current_crypted)

    return tuple(cryptogram)


def decrypt(encrypted: tuple, public_key: tuple, modulus: int, prime: int) -> str:
    """
    Decrypts a message.

    Args:
        encrypted (tuple): The encrypted message
        public_key (tuple): The public key
        modulus (int): The modulus number
        prime (int): The prime number

    Returns:
        str: The decrypted message
    """

    # We compute the inverse of the prime number modulo the modulus number
    inverse_prime: Final[int] = euclid(modulus, prime)

    # We compute the reminders
    reminders: Final[Iterable[int]] = (elem * inverse_prime % modulus for elem in encrypted)

    # We apply the knapsack algorithm to each reminder
    knapsacked: Final[Iterable[str]] = (knapsack(public_key, elem) for elem in reminders)

    # We convert the binary numbers to decimal
    binary: Final[Iterable[str]] = chain.from_iterable(wrap(elem, 5) for elem in knapsacked)
    decimal: Final[Iterable[int]] = (int(elem, 2) for elem in binary)

    # We convert the decimal numbers to characters
    decrypted: Final[Iterable[str]] = (inverse_character_map(elem) for elem in decimal)

    return array_to_string(decrypted)


############################################
## Here you can change the encryption key ##
############################################

PRIVATE_KEY: Final[tuple] = (1, 3, 5, 11, 21, 44, 87, 175, 349, 701)
MODULUS: Final[int] = 1590
PRIME: Final[int] = 43

#######################################
## Here you can change the plaintext ##
#######################################

PLAIN_TEXT: str = 'ANA ARE MERE'
PLAIN_TEXT = validate_text(PLAIN_TEXT)

# We define the ASCII offset
ASCII_OFFSET: Final[int] = ord('A')

# We compute the public key
PUBLIC_KEY: Final[tuple] = generate_public_key(PRIVATE_KEY, MODULUS, PRIME)

# We encrypt the plaintext
ENCYPTED: Final[tuple] = encrypt(PLAIN_TEXT, PUBLIC_KEY)

# We decrypt the encrypted text
DECRYPTED: Final[str] = decrypt(ENCYPTED, PRIVATE_KEY, MODULUS, PRIME)

# We print the results
print(F'The private key is: {PRIVATE_KEY}')
print(F'The modulus number is: {MODULUS}')
print(F'The prime number is: {PRIME}')
print(F'The public key is: {PUBLIC_KEY}')
print(F'The message is: {PLAIN_TEXT}')
print(F'The encrypted message is: {ENCYPTED}')
print(F'The decrypted message is: {DECRYPTED}')
