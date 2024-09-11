import functools
import string
import collections
import argparse

"""This module contains functions to count the number of symbols in a text."""

group_1 = string.ascii_uppercase + '_' + string.digits
group_2 = string.ascii_lowercase + '_' + string.digits
group_3 = string.punctuation + ' '


def count_symbols(text: collections.Counter) -> dict:
    """This function adds all symbols to a dictionary."""
    counter = collections.Counter(text)
    return counter


@functools.cache
def counting_symbols(text, categories: dict | None = None
                     ) -> dict:
    if not isinstance(text, str):
        raise TypeError(f"text must be a string, but got {type(text)}")
    elif not categories:
        categories = {
            "all_symbols": group_1,
            "words_symbols": group_2,
            "punctuation_and_spaces": group_3
        }
    symbols = count_symbols(text)
    result = {}
    for symbol, count in symbols.items():
        for name, category in categories.items():
            if symbol in category and count == 1:
                result[name] = result.get(name, 0) + 1
    return result

def parse_func():
    parser = argparse.ArgumentParser(prog="Рахувалка унікальних символів",
                                     description="Ця програма рахує кількість унікальних символів у введеному тексті",
                                     epilog="Thats all!")
    parser.add_argument("-s", "--string", help="Текст, який буде передано в функцію")
    parser.add_argument("-f", "--file", type=argparse.FileType('r'),
                                                    help="Вкажіть шлях до файлу")
    return parser.parse_args()
def cli_interface():
    """This function """
    args = parse_func()
    if args.file:
        read_data = args.file.read()
        return read_data
    elif args.string:
        return args.string
    else:
        raise ValueError("Ведені некоректні дані")



if __name__ == "__main__":
    data = cli_interface()
    print(counting_symbols(data))
