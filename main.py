import sys
import json
import pandas as pd
import traceback
from datatypes import BedsRecord, BedTypesData
from enum import Enum
from api import sendBedsData


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
    EXPORT_FILENAME = './export/#.json'
    BED_RECORDS_NUMBER = 24


TOP_N = 10
MENU = [
    '''Please enter the desired option: 

    (1) Global bed capacity
    (2) Measures and restrictions by country
    (0) Exit program''',
    '''\nBeds dataset chosen. What filter would you like to apply?

    (1) Number and percentage of beds per type, by country (scale)
    (2) Top 10 countries with higher bed capacity (scale)
    (3) Top 10 countries with lower bed capacity (scale)
    (4) Top 10 countries with higher bed capacity (estimated total)    
    (5) Top 10 countries with lower bed capacity (estimated total)
    (0) Go back''',
    '''\nMeasures dataset chosen. What filter would you like to apply?

    (...) Yet to implement''',
    '''\nDo you want to send the results to the API?
    Type "yes" if you want to; otherwise, hit the Enter (Return) key
    '''
]


def prompt_user(message):
    """
    Prompts the user with a message to input data and returns it
    """
    print(message)
    return input()


def process_without_filter(data):
    """
    Returns the basic structure of the whole dataset without filter    
    """    
    country_gb = data.groupby('country')

    return(pack_records(country_gb))


def process_by_scale_capacity(data, ascending = False):
    """
    Filters by the N top or bottom countries by bed count and returns the list
    of filtered BedsRecords
    Precondition: The beds_total column has been added to the dataframe
    """    
    sorted_data = data.sort_values(['beds_total'], ascending = ascending)
    country_gb = sorted_data.groupby(['beds_total','country'], sort = False)

    return pack_records(country_gb, TOP_N)


def process_by_estimated_capacity(data, ascending = False):
    """
    Filters by the N top or bottom countries by bed estimate and returns the
    list of filtered BedsRecords
    Precondition: The estimated_beds_total column has been added to the
    dataframe
    """
    sorted_data = data.sort_values(['estimated_beds_total'], 
                                   ascending = ascending)
    country_gb = sorted_data.groupby(['estimated_beds_total','country'],
                                     sort = False)

    return pack_records(country_gb, TOP_N)


def filter_beds(category, sampling = False):
    """
    Returns the dataset (pandas.core.frame.DataFrame) filtered by the input
    filter category. If the sampling parameter is set to true, only a number
    of records will be taken from the dataset according to the value of the
    BedsFilter.BED_RECORDS_NUMBER constant
    The returned structure is a list with three elements:
    [0]: General structure for country information
    [1]: Information for bed types
    """
    try:
        data = pd.read_csv(BedsFilter.BEDS_FILENAME.value)

        if sampling:
            data = data.head(BedsFilter.BED_RECORDS_NUMBER.value)

        data['estimated_beds'] = data['population'] * data['beds'] / 10
        data['estimated_beds_total'] = data.groupby('country') \
                                                ['estimated_beds'] \
                                           .transform('sum')
        data['estimated_beds_average'] = data.groupby('country') \
                                                ['estimated_beds'] \
                                            .transform('mean')
        data['beds_total'] = data.groupby('country')['beds'].transform('sum')
        data['beds_average'] = data.groupby('country')['beds'] \
                                  .transform('mean')
        data['population_average'] = data.groupby('country')['population'] \
                                         .transform('mean')
        
        if (category == BedsFilter.NUMBER_PERCENT_COUNTRY_NORMAL.value):
            return process_without_filter(data)
        elif (category == BedsFilter.TOP_COUNTRIES_BY_SCALE.value):
            return process_by_scale_capacity(data)
        elif (category == BedsFilter.BOTTOM_COUNTRIES_BY_SCALE.value):
            return process_by_scale_capacity(data, True)
        elif (category == BedsFilter.TOP_COUNTRIES_BY_ESTIMATE.value):            
            return process_by_estimated_capacity(data)
        elif (category == BedsFilter.BOTTOM_COUNTRIES_BY_ESTIMATE.value):            
            return process_by_estimated_capacity(data, True)
        elif (category == BedsFilter.NUMBER_PERCENT_COUNTRY_NORMAL.value):
            raise Exception("Not implemented yet")
    except FileNotFoundError:
        print(f'The file "{BedsFilter.BEDS_FILENAME.value}" does not exist')    


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


def pack_records(country_gb, limit = None):
    """
    From a filtered grouped dataframe, return a list of BedsRecords and 
    BedsTypesData. If a limit is entered, only return the first elements up to
    one before that limit
    Precondition: The dataset contains the beds_total, beds_average,
    population_average, estimated_beds, estimated_beds_total, and
    estimated_beds_average columns
    """
    result = []

    country_records = []
    type_records = []
    
    for country_name, country_group in [g for g in list(country_gb)[:limit]]:
        beds_average = country_group['beds_average'].values[0]
        beds_total = country_group['beds_total'].values[0]
        population = country_group['population_average'].values[0]
        estimated_beds_total = country_group['estimated_beds_total'].values[0]
        estimated_beds_average = country_group['estimated_beds_average'] \
                                     .values[0]
        iso_code = ""

        if (type(country_name) is tuple):
            iso_code = country_name[1].lower()
        else:
            iso_code = country_name.lower()

        new_record = BedsRecord(code = iso_code,
                                lat = float(country_group['lat'].values[0]),
                                lng = float(country_group['lng'].values[0]),
                                beds_total = float(beds_total),
                                beds_average = float(beds_average),
                                estimated_beds_total = \
                                    float(estimated_beds_total),
                                estimated_beds_average = \
                                    float(estimated_beds_average),
                                population_average = population)

        bed_types_groups = country_group.groupby('type')

        for type_name, type_group in bed_types_groups:
            type_bed_count = float(type_group['beds'].values[0])
            type_percentage = 100 * type_bed_count / beds_total
            type_population = float(type_group['population'].values[0])
            type_estimated = type_population * type_bed_count / 10
            source = type_group['source'].values[0]
            source_url = type_group['source_url'].values[0]
            year = type_group['year'].values[0]

            new_type_data = BedTypesData(code = iso_code,
                                         type_name = type_name.lower(),
                                         count = type_bed_count,
                                         percentage = type_percentage,
                                         estimated_for_population = \
                                             type_estimated,
                                         population = type_population,
                                         source = source,
                                         source_url = source_url,
                                         year = int(year))

            type_records.append(new_type_data)

        country_records.append(new_record)

    if (limit != None):
        country_records = country_records[:limit]
    
    return [country_records, type_records]


def write_to_file(data, filename):
    try:
        with open(filename, 'w') as export_file:
            export_file.write(data)
        print(f'Wrote the results on {filename}!')
    except OSError as e:
        print(f'Could not write {filename}!')
        print(e)


def write_data(general_json, types_json, filterIndex):
    """
    Writes the entered json into a file named according to the chosen filter
    """
    general_name = BedsFilter(filterIndex).name + '_GENERAL'
    types_name = BedsFilter(filterIndex).name + '_TYPES'
    general_filename = BedsFilter.EXPORT_FILENAME.value.replace("#", 
                                                                general_name)
    types_filename = BedsFilter.EXPORT_FILENAME.value.replace("#", types_name)
    
    write_to_file(general_json, general_filename)
    write_to_file(types_json, types_filename)


def load_records(filter_option, cli_mode = False, send_request = False):
    """
    Retrieves filtered record, and writes their data on JSON files or sends to 
    backend API according to the specified parameters
    If CLI mode is enabled, the user will be prompted to choose whether a
    request will be sent to the API; otherwise, the sending must be specified
    through the send_request parameter
    """
    records = filter_beds(filter_option)

    general_json_list = [r.to_json()
                            for r in records[0]]
    types_json_list = [r.to_json()
                        for r in records[1]]

    general_data = json.dumps(general_json_list, indent = 4)
    types_data = json.dumps(types_json_list, indent = 4)

    api_data = [general_data, types_data]

    write_data(general_data, types_data, filter_option)

    if (cli_mode):
        user_input = prompt_user(MENU[3])
        answer = user_input.lower() == 'yes'
        
        if (answer):
            sendBedsData(api_data)

    elif (send_request):
        sendBedsData(api_data)


def main_cli():
    """
    Program entry point without execution arguments
    """
    finished = False
    dataset_option = 0
    filter_option = 0
        
    while (not finished):
        filter_navigation = True        
        dataset_option = int(prompt_user(MENU[0]))
        
        if (validate_option(dataset_option, 0, 2)):
            if (dataset_option == 0):
                finished = True 
            elif (dataset_option == 1):
                while (filter_navigation):
                    filter_option = int(prompt_user(MENU[1]))

                    if (validate_option(filter_option, 0, 5)):
                        if (filter_option == 0):
                            filter_navigation = False
                        else:
                            load_records(filter_option, cli_mode = True)
            else:
                raise Exception("Not implemented yet")


def main_args(send_request = False):
    """
    Program entry point with execution arguments
    """    
    dataset_option = int(sys.argv[1])

    if (validate_option(dataset_option, 1, 2)):
        if (dataset_option == 1):
            filter_option = int(sys.argv[2])

            if (validate_option(filter_option, 1, 5)):
                load_records(filter_option, send_request = send_request)
        else:
            raise Exception("Not implemented yet")


if __name__ == "__main__":
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