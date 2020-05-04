import sys
from beds_data import BedsRecord, BedTypesData
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
    BED_RECORDS_NUMBER = 24


MENU = [
    '''Please enter the desired option: 

    (1) Global bed capacity
    (2) Measures and restrictions by country
    (0) Exit program''',
    '''\nBeds dataset chosen. What filter would you like to apply?

    (1) Number and percentage of beds per type, by country (scale)
    (2) Top 10 countries with higher bed capacity (scale)
    (3) Top 10 countries with higher bed capacity (estimated total)
    (4) Top 10 countries with lower bed capacity (scale)
    (5) Top 10 countries with lower bed capacity (estimated total)
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
        data = pd.read_csv(BedsFilter.BEDS_FILENAME.value) \
                   .head(BedsFilter.BED_RECORDS_NUMBER.value)
        ## TODO: Remove head for processing the full dataset
        if (category == BedsFilter.NUMBER_PERCENT_COUNTRY_NORMAL.value):
            return process_without_filter(data)
        elif (category == BedsFilter.TOP_COUNTRIES_BY_SCALE.value):
            return process_by_scale_capacity(data)
        elif (category == BedsFilter.BOTTOM_COUNTRIES_BY_SCALE.value):
            return process_by_scale_capacity(data, False)
        elif (category == BedsFilter.TOP_COUNTRIES_BY_ESTIMATE.value):
            raise Exception("Not implemented yet")
        elif (category == BedsFilter.BOTTOM_COUNTRIES_BY_ESTIMATE.value):
            raise Exception("Not implemented yet")
        elif (category == BedsFilter.NUMBER_PERCENT_COUNTRY_NORMAL.value):
            raise Exception("Not implemented yet")
    except FileNotFoundError:
        print(f'The file "{BedsFilter.BEDS_FILENAME.value}" does not exist')
    except Exception as e:
        print(e)


def validate_option(option, min_value, max_value):
    if (option >= min_value and option <= max_value):
        return True
    else:
        print('\nNot a valid option! Try again\n')
        return False


def process_without_filter(data):
    """
    Returns the basic structure of the whole dataset as a list of BedsRecords
    """
    records = []

    country_data = data.groupby('country')

    for country_name, country_group in country_data:
        beds_average = country_group['beds'].mean()
        beds_total = country_group['beds'].sum()
        population = country_group['population'].mean()
        bed_types_list = country_group['beds']        

        new_record = BedsRecord(code = country_name.lower(),
                                lat = float(country_group['lat'].values[0]),
                                lng = float(country_group['lng'].values[0]),
                                beds_total = float(beds_total),
                                beds_average = float(beds_average),
                                population_average = population)

        bed_types_objects = []
        
        bed_types_groups = country_group.groupby('type')

        estimated_beds_total = 0
        types_number = 0

        for type_name, type_group in bed_types_groups:
            type_bed_count = float(type_group['beds'].values[0])
            type_percentage = 100 * type_bed_count / beds_total
            type_population = float(type_group['population'].values[0])
            type_estimated = type_population * type_bed_count / 10
            source = type_group['source'].values[0]
            source_url = type_group['source_url'].values[0]
            year = type_group['year'].values[0]

            new_type_data = BedTypesData(type_name = type_name.lower(), \
                                         count = type_bed_count, \
                                         percentage = type_percentage, \
                                         estimated_for_population = \
                                             type_estimated, \
                                         population = type_population, \
                                         source = source, \
                                         source_url = source_url, \
                                         year = int(year))

            new_record.add_bed_type(new_type_data.getStructure())

            estimated_beds_total += type_estimated
            types_number += 1

        new_record.set_estimated_beds_total(estimated_beds_total)
        new_record.set_estimated_beds_average(estimated_beds_total, types_number)

        records.append(new_record)

    return records


def process_by_scale_capacity(data, descending = True):
    """
    Filters by the N top or bottom countries by bed count and returns the list
    of the filtered BedsRecords
    """
    records = []

    data['bedsAverage'] = data.groupby('country')['beds'].transform('mean')
    data['bedsTotal'] = data.groupby('country')['beds'].transform('sum')
    data['populationAverage'] = data.groupby('country')['population'].transform('mean')
    data['populationAverage'] = data.groupby('country')['population'].transform('mean')


    country_data = data.groupby('country')

    for country_name, country_group in country_data:
        beds_average = country_group['beds'].mean()
        beds_total = country_group['beds'].sum()
        population = country_group['population'].mean()
        bed_types_list = country_group['beds']        

        new_record = BedsRecord(code = country_name.lower(),
                                lat = float(country_group['lat'].values[0]),
                                lng = float(country_group['lng'].values[0]),
                                beds_total = float(beds_total),
                                beds_average = float(beds_average),
                                population_average = population)

        bed_types_objects = []
        
        bed_types_groups = country_group.groupby('type')

        estimated_beds_total = 0
        types_number = 0

        for type_name, type_group in bed_types_groups:
            type_bed_count = float(type_group['beds'].values[0])
            type_percentage = 100 * type_bed_count / beds_total
            type_population = float(type_group['population'].values[0])
            type_estimated = type_population * type_bed_count / 10
            source = type_group['source'].values[0]
            source_url = type_group['source_url'].values[0]
            year = type_group['year'].values[0]

            new_type_data = BedTypesData(type_name = type_name.lower(), \
                                         count = type_bed_count, \
                                         percentage = type_percentage, \
                                         estimated_for_population = \
                                             type_estimated, \
                                         population = type_population, \
                                         source = source, \
                                         source_url = source_url, \
                                         year = int(year))

            new_record.add_bed_type(new_type_data.getStructure())

            estimated_beds_total += type_estimated
            types_number += 1

        new_record.set_estimated_beds_total(estimated_beds_total)
        new_record.set_estimated_beds_average(estimated_beds_total, types_number)

        records.append(new_record)

    return records


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
                                records = filter_beds(filter_option)

                                print('\nResults for the chosen filter\n')
                                print(str(records))

                else:
                    raise Exception("Not implemented yet")
        except ValueError:
            print('\nSorry, only numbers are valid! Try again\n')
        except Exception as e:            
            traceback.print_exc()
            sys.exit(f'An error happened! \n {e} \n')


if __name__ == "__main__":
    main()