import string
import random


def get_random_characters(length=5):
    characters = (
        string.ascii_letters + string.digits
    )  # Includes both letters and digits
    return "".join(random.choices(characters, k=length))
