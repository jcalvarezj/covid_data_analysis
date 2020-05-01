import os
from beds import BedsRecord
from enum import Enum
import pandas as pd


class BED_FILTER_CATEGORIES(Enum):
    """
    Enum that provides constant integers to describe category filters for the
    beds dataset
    """
    NUMBER_PERCENT_COUNTRY_NORMAL = 1
    TOP_COUNTRIES_BY_SCALE = 2
    BOTTOM_COUNTRIES_BY_SCALE = 3
    TOP_COUNTRIES_BY_ESTIMATE = 4
    BOTTOM_COUNTRIES_BY_ESTIMATE = 5


BEDS_FILENAME = './data/hospital_beds.csv'
MENU = [
    '''Please enter the dataset to process or x to exit: 

    (1) Global bed capacity
    (2) Measures and restrictions by country
    (0) Exit program''',
    '''\nBeds dataset chosen. What filter would you like to apply?

    (1) No filter; bring all data as JSON
    (2) Number and percentage of beds per type, by country (scale)
    (3) Top 10 countries with higher bed capacity (scale)
    (4) Top 10 countries with higher bed capacity (estimated total)
    (5) Top 10 countries with lower bed capacity (scale)
    (6) Top 10 countries with lower bed capacity (estimated total)
    (0) Go back''',
    '''\nMeasures dataset chosen. What filter would you like to apply?

    (...) Yet to implement
    E(x)it'''
]


def prompt_user(message):
    """
    Prompts the user with a message to input data and returns it 
    """
    print(message)
    return input()


def filter_beds(category):
    try:
        data = pd.read_csv(BEDS_FILENAME)
        print(data)
        print(f'USING CATEGORY {category}')
    except FileNotFoundError:
        print(f'The file "{BEDS_FILENAME}" does not exist')


def validate_option(option, min_value, max_value):
    if (option >= min_value and option <= max_value):
        return True
    else:
        print('\nNot a valid option! Try again\n')
        return False


def main():
    finished = False
    dataset_option = 0
    filter_option = 0
        
    while (not finished):
        filter_navigation = True

        try:
            dataset_option = int(prompt_user(MENU[0]))
            
            if (validate_option(dataset_option, 0, 2)):
                if (dataset_option == 0):
                    finished = True 
                elif (dataset_option == 1):
                    while (filter_navigation):
                        filter_option = int(prompt_user(MENU[1]))

                        if (validate_option(filter_option, 0, 6)):
                            if (filter_option == 0):
                                filter_navigation = False
                            else:
                                filter_beds(filter_option)
                else:
                    print("\n*** YET TO IMPLEMENT ***\n")
        except ValueError:
            print('\nSorry, only numbers are valid! Try again\n')


if __name__ == "__main__":
    main()