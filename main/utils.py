"""
Module with utility functions.
"""
import random


def shuffle_str(string: str) -> str:
    """
    Shuffle random string.
    """
    str_var = list(string)
    random.shuffle(str_var)
    return "".join(str_var)
