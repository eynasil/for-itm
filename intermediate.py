# Anasel-Ace M. Cañeso, 221473
# 11 March 2024
# Python: Intermediate

def shift_letter(letter, shift):
    letters = (
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    )

    if letter == " ":
        return " "
    elif letter in letters:
        return letters[(letters.index(letter) + shift) % len(letters)]
        

def caesar_cipher(message, shift):
    message = ""
    letters = (
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    )

    for letter in message:
        if letter == " ":
            new_message += " "
        elif letter in letters:
            new_message += letters[(letters.index(letter) + shift) % len(letters)]
    
    return new_message


def shift_by_letter(letter, letter_shift):
    letters = (
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    )

    if letter == " ":
        return " "
    elif letter in letters:
        return letters[(letters.index(letter) + letters.index(letter_shift)) % len(letters)]


def vigenere_cipher(message, key):
    new_message = ""
    key = key * ((len(message) // len(key)) + 1)
    letters = (
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    )
    
    for index, letter in enumerate(message):
        if letter == " ":
            new_message += " "
        elif letter in letters:
            new_message += letters[(letters.index(letter) + letters.index(key[index])) % len(letters)]
    
    return new_message  


def scytale_cipher(message, shift):
    encoded_message = ""
    if len(message) % shift != 0:
        message += '_' * (shift - (len(message) % shift))

    for i in range(len(message)):
        index = (i // shift) + (len(message) // shift) * (i % shift)
        encoded_message += message[index]

    return encoded_message


def scytale_decipher(message, shift):
    rows = len(message) // shift
    cols = (len(message) // rows) + (1 if len(message) % rows != 0 else 0)

    decoded_message = [""] * len(message)

    k = 0
    for j in range(cols):
        for i in range(rows):
            index = i * cols + j
            if index < len(message):
                decoded_message[k] = message[index]
                k += 1

    return "".join(decoded_message)

"""
I hereby attest to the truth of the following facts:

I have not discussed the Python code in my program with anyone other than my instructor or the teaching assistants assigned to this course.

I have not used Python code obtained from another student, or any other unauthorized source, whether modified or unmodified.

If any Python code or documentation used in my program was obtained from another source, it has been clearly noted with citations in the comments of my program.
"""
