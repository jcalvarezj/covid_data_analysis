"""
This is the main module of the application that serves as execution entry point
"""

import sys
import beds
import traceback
import measures as msrs
from commons import prompt_user
from constants import MENU, BED_FILTERS, MEASURE_FILTERS


def validate_option(option, min_value, max_value):
    """
    Validates whether an option number is in the accepted interval (between
    min_value and max_value)
    """
    if (option >= min_value and option <= max_value):
        return True
    else:
        print('\nNot a valid option! Try again\n')
        return False


def main_cli():
    """
    Program entry point without execution arguments
    """
    finished = False
    dataset_option = 0
    filter_option = 0

    while (not finished):
        filter_navigation = True        
        dataset_option = int(prompt_user(0))

        if (validate_option(dataset_option, 0, 2)):
            if (dataset_option == 0):
                finished = True 
            elif (dataset_option == 1):
                while (filter_navigation):
                    filter_option = int(prompt_user(1))

                    if (validate_option(filter_option, 0, len(BED_FILTERS))):
                        if (filter_option == 0):
                            filter_navigation = False
                        else:
                            beds.load_bed_records(filter_option,
                                                  cli_mode = True)
            else:
                while (filter_navigation):
                    filter_option = int(prompt_user(2))

                    if (validate_option(filter_option, 0, 
                                        len(MEASURE_FILTERS))):
                        if (filter_option == 0):
                            filter_navigation = False
                        else:
                            msrs.load_measure_records(filter_option,
                                                      cli_mode = True)


def main_args(send_request = False):
    """
    Program entry point with execution arguments
    """    
    dataset_option = int(sys.argv[1])

    if (validate_option(dataset_option, 1, 2)):
        if (dataset_option == 1):
            filter_option = int(sys.argv[2])

            if (validate_option(filter_option, 1, len(BED_FILTERS))):
                beds.load_bed_records(filter_option,
                                      send_request = send_request)
        else:
            filter_option = int(sys.argv[2])

            if (validate_option(filter_option, 1, len(MEASURE_FILTERS))):
                msrs.load_measure_records(filter_option,
                                          send_request = send_request)


if __name__ == '__main__':
    try:
        if (len(sys.argv) == 1):
            main_cli()
        elif (len(sys.argv) == 3):
            main_args()
        elif (len(sys.argv) == 4):
            main_args(sys.argv[3] == 'post')
        else:
            raise Exception('Not enough arguments. Usage: python main.py' \
                +' <index of dataset> <index of filter>')
    except ValueError:        
        print('\nSorry, only numbers are valid! Try again\n')
    except Exception as e:
        traceback.print_exc()
        sys.exit(f'\nUnexpected error! Exiting.\nThe error: ** {e} ** \n')