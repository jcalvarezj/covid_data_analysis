"""
This module includes common functions used by different modules
"""

from constants import MENU, BED_FILTERS, MEASURE_FILTERS


def _print_filters(filters):
    """
    Prints the filters as menu options on the CLI
    """
    count = 1
    for f in filters:
        print(f'    ({count}) {f}')
        count += 1
    print('    (0) Go back\n')


def prompt_user(message_index):
    """
    Prompts the user with a message to input data and returns it
    """
    print(MENU[message_index])
    if (message_index == 1):
        _print_filters(BED_FILTERS)
    elif (message_index == 2):
        _print_filters(MEASURE_FILTERS)
    return input()