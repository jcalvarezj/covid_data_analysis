import os
from beds import BedsRecord
from enum import Enum
import pandas as pd
import traceback


class BedsFilter(Enum):
    """
    Enum that provides constant integers to describe category filters for the
    beds dataset
    """
    NUMBER_PERCENT_COUNTRY_NORMAL = 1
    TOP_COUNTRIES_BY_SCALE = 2
    BOTTOM_COUNTRIES_BY_SCALE = 3
    TOP_COUNTRIES_BY_ESTIMATE = 4
    BOTTOM_COUNTRIES_BY_ESTIMATE = 5
    TOP_COUNTRIES_BY_AVERAGE = 6
    BOTTOM_COUNTRIES_BY_AVERAGE = 7


BEDS_FILENAME = './data/hospital_beds.csv'
MENU = [
    '''Please enter the desired option: 

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

    (...) Yet to implement'''
]


def prompt_user(message):
    """
    Prompts the user with a message to input data and returns it 
    """
    print(message)
    return input()


def filter_beds(category):
    """
    Returns the dataset (pandas.core.frame.DataFrame) filtered by the input
    filter category
    """
    try:
        data = pd.read_csv(BEDS_FILENAME)
        if (category == BedsFilter.NUMBER_PERCENT_COUNTRY_NORMAL.value):
            return data
        elif (category == BedsFilter.TOP_COUNTRIES_BY_SCALE.value):
            raise Exception("Not implemented yet")
        elif (category == BedsFilter.BOTTOM_COUNTRIES_BY_SCALE.value):
            raise Exception("Not implemented yet")
        elif (category == BedsFilter.TOP_COUNTRIES_BY_ESTIMATE.value):
            raise Exception("Not implemented yet")
        elif (category == BedsFilter.BOTTOM_COUNTRIES_BY_ESTIMATE.value):
            raise Exception("Not implemented yet")
        elif (category == BedsFilter.NUMBER_PERCENT_COUNTRY_NORMAL.value):
            raise Exception("Not implemented yet")
    except FileNotFoundError:
        print(f'The file "{BEDS_FILENAME}" does not exist')
    except Exception as e:
        print(e)


def validate_option(option, min_value, max_value):
    if (option >= min_value and option <= max_value):
        return True
    else:
        print('\nNot a valid option! Try again\n')
        return False


def process_raw_data(data):
    records = []

    country_data = data.groupby('country')

    for name, group in country_data:
        print(name)
        print('--------')
        print(group)
        print('--------\n\n')

        beds_average = group['beds'].mean()

        population = group['population'].mean()

        # print(f'Promedio de camas para {name}: {beds_average}')

        bed_type = group['beds']

        bed_type_count = bed_type.sum()

        # print(f'Los tipos para {name} son\n{bed_type} de total {bed_type_count}')


        # print(f'Las coordenadas de {name} son {group.lat[0]} {group.lng[0]}')

        # print(f"CREANDO REGISTRO PARA {name} ... grupo: {group.values[0]}")

        new_record = BedsRecord(code = name.lower(),
                                lat = float(group.lat.values[0]),
                                lng = float(group.lng.values[0]),
                                beds_average = float(beds_average),
                                population = population,
                                estimated_beds_average = float(beds_average))

        print(f'MI NUEVO REGISTRO ES!!! ')
        print(new_record)        

        # records.append(new_record)


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
                                raw_data = filter_beds(filter_option).head(6)

                                records = process_raw_data(raw_data)
                else:
                    raise Exception("Not implemented yet")
        except ValueError:
            print('\nSorry, only numbers are valid! Try again\n')
        except Exception as e:
            print("An error happened!")
            print(e)
            traceback.print_exc()


if __name__ == "__main__":
    main()