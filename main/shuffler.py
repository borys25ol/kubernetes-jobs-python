"""
Module with cli functions.
"""
import click
from log import get_logger
from utils import shuffle_str

logger = get_logger(name="shuffler")


@click.command()
@click.argument("input_string")
def shuffle_string(input_string: str) -> None:
    if isinstance(input_string, str):
        if len(input_string) < 2:
            raise ValueError("Must be at least 2 characters.")

        logger.info(f"Original string: {input_string}")

        shuffled_string = shuffle_str(string=input_string)
        logger.info(f"Shuffled string: {shuffled_string}")
    else:
        raise ValueError("Input must be a string.")


if __name__ == "__main__":
    shuffle_string()
