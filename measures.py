"""
This module contains functions for processing the measures/restrictions dataset
"""

import api
import json
import pycountry
import pandas as pd
from commons import prompt_user
from datatypes import MeasuresData
from file_export import write_measures_data
from constants import MeasuresFilter, TOP_N, REMAINING_ISO_CODES


def _country_to_iso(country):
    """
    Returns the ISO 3166 - alpha 2 code for a given country name
    """
    if (country.startswith('US:')):
      return 'US'
    else:
        result = pycountry.countries.get(name = country)
        if (not result):
          return REMAINING_ISO_CODES[country]
        else:
          return result.alpha_2


def transform_measures_dataset(data):
    """
    Deletes records with empty values on the 'Keywords' and 'Country' columns,
    and adds the 'Code' column with the ISO 3166 - alpha 2 code of the country
    names in 'Country'
    """
    data = data.dropna(subset = ['Keywords', 'Country'])
    data['Code'] = data.apply(_country_to_iso)

    return data


def filter_measures(category, sampling = False):
    """
    Returns the dataset (pandas.core.frame.DataFrame) filtered by the input
    filter category. If the sampling parameter is set to true, only a number
    of records will be taken from the dataset according to the value of the
    BedsFilter.SAMPLE_RECORDS constant
    The returned structure is a list with two elements:
    [0]: General structure for country information
    [1]: Information for bed types
    """
    try:
        data = pd.read_csv(MeasuresFilter.DATA_FILENAME.value)

        if sampling:
            data = data.head(Measures.SAMPLE_RECORDS.value)

        transform_measures_dataset(data)
        
        if (category == MeasuresFilter.GENERAL_COUNTRY_INFORMATION.value):
            raise Exception("Not implemented yet")
        else:
            raise Exception("Not implemented yet")
    except FileNotFoundError:
        print(f'The file "{BedsFilter.DATA_FILENAME.value}" does not exist')


def load_measure_records(filter_option, cli_mode = False, sampling = False,
                         send_request = False):
    """
    Retrieves filtered measures and restrictions records and writes their data
    on JSON files or sends them to the backend's API according to the specified
    parameters
    If CLI mode is enabled, the user will be prompted to choose whether a
    request will be sent to the API; otherwise, the sending must be specified
    through the send_request parameter
    """    
    records = filter_measures(filter_option, sampling)
    
    general_json_list = records[0].to_json() \
        if (filter_option == MeasuresFilter.GENERAL_STATISTICS.value) \
        else [r.to_json() for r in records[0]]

    types_json_list = [r.to_json()
                        for r in records[1]]

    general_data = json.dumps(general_json_list, indent = 4)
    types_data = json.dumps(types_json_list, indent = 4)

    api_data = [general_data, types_data]

    write_measures_data(general_data, types_data, filter_option)

    if (cli_mode):
        user_input = prompt_user(3)
        answer = user_input.lower() == 'yes'

        if (answer):
            api.send_measures_data(api_data)
    elif (send_request):
        api.send_measures_data(api_data)