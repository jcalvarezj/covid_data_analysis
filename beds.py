"""
This module contains functions for processing the bed capacity dataset
"""

import sys
import api
import json
import pandas as pd
from file_export import write_beds_data
from commons import prompt_user
from constants import BedsFilter, TOP_N
from datatypes import (BedsRecord, BedTypesData, BedsGeneralData,
                       BedTypesGeneralData)


def _pack_records(country_gb):
    """
    From a filtered grouped dataframe, returns a list of BedsRecords and
    BedsTypesData objects
    Precondition: The dataset contains the beds_total, beds_average,
    population_average, estimated_beds, estimated_beds_total, and
    estimated_beds_average columns
    """
    country_records = []
    type_data = []

    for country_name, country_group in country_gb:
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

            type_data.append(new_type_data)

        country_records.append(new_record)

    return [country_records, type_data]


def _process_without_filter(data):
    """
    Returns the basic structure of the whole dataset without filter
    """
    country_gb = data.groupby('country')
    return(_pack_records(country_gb))


def _process_by_scale_capacity(data, ascending = False):
    """
    Filters by the N top or bottom countries by bed count and returns the list
    of filtered BedsRecords
    Precondition: The beds_total column has been added to the dataframe
    """
    sorted_data = data.sort_values(['beds_total'], ascending = ascending)
    country_gb = sorted_data.groupby(['beds_total','country'], sort = False)

    return _pack_records(country_gb, TOP_N)


def _process_by_estimated_capacity(data, ascending = False):
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

    return _pack_records(country_gb, TOP_N)


def _process_by_average_scale_capacity(data, ascending = False):
    """
    Filters by the N top or bottom countries by bed estimate and returns the
    list of filtered BedsRecords
    Precondition: The beds_average column has been added to the
    dataframe
    """
    sorted_data = data.sort_values(['beds_average'], 
                                   ascending = ascending)
    country_gb = sorted_data.groupby(['beds_average','country'],
                                     sort = False)

    return _pack_records(country_gb, TOP_N)


def _process_by_average_estimated_capacity(data, ascending = False):
    """
    Filters by the N top or bottom countries by bed estimate and returns the
    list of filtered BedsRecords
    Precondition: The estimated_beds_average column has been added to the
    dataframe
    """
    sorted_data = data.sort_values(['estimated_beds_average'], 
                                   ascending = ascending)
    country_gb = sorted_data.groupby(['estimated_beds_average','country'],
                                     sort = False)

    return _pack_records(country_gb, TOP_N)


def _process_general_statistics(beds_df):
    """
    Retrieves the dataset's general statistics in a list of two elements:
    [0] General information
    [1] Type-specific information
    """
    beds_total = float(beds_df['beds_total'].sum())
    beds_average = float(beds_df['beds_total'].mean())
    beds_std = float(beds_df['beds_total'].std())
    raw_sources_count = dict(beds_df['source'].value_counts())

    sources_count = {source: int(count) for source, count
                     in raw_sources_count.items()}

    general_data = BedsGeneralData(beds_total, beds_average, beds_std,
                                   sources_count)
    types_data = []
    types_gb = beds_df.groupby('type')

    for type_name, type_group in types_gb:
        type_count = float(type_group['beds'].sum())
        type_percentage = float(type_count / beds_total * 100)
        type_average = float(type_group['beds'].mean())
        type_std = float(type_group['beds'].std())
        if (pd.isna(type_std)):
            type_std = 0.0

        types_record = BedTypesGeneralData(type_name.lower(), type_count,
                                           type_percentage, type_average,
                                           type_std)
        types_data.append(types_record)

    return [general_data, types_data]


def _transform_beds_dataset(data):
    """
    Includes additional columns to the beds dataset:
    - estimated_beds: the amount of beds per person
    - estimated_beds_total: sum of all estimated_beds in a country groupby
    - estiamted_beds_average: average of estimated_beds in a country groupby
    - beds_total: sum of beds in a country groupby
    - beds_total: average of beds in a country groupby
    """
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


def _filter_beds(category, sampling = False):
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
        data = pd.read_csv(BedsFilter.DATA_FILENAME.value)

        if sampling:
            data = data.head(BedsFilter.SAMPLE_RECORDS.value)

        _transform_beds_dataset(data)

        if (category == BedsFilter.NUMBER_PERCENT_COUNTRY_NORMAL.value):
            return _process_without_filter(data)
        elif (category == BedsFilter.TOP_COUNTRIES_SCALE.value):
            return _process_by_scale_capacity(data)
        elif (category == BedsFilter.BOTTOM_COUNTRIES_SCALE.value):
            return _process_by_scale_capacity(data, True)
        elif (category == BedsFilter.TOP_COUNTRIES_ESTIMATE.value):
            return _process_by_estimated_capacity(data)
        elif (category == BedsFilter.BOTTOM_COUNTRIES_ESTIMATE.value):
            return _process_by_estimated_capacity(data, True)
        elif (category == BedsFilter.TOP_COUNTRIES_AVG_SCALE.value):
            return _process_by_average_scale_capacity(data)
        elif (category == BedsFilter.BOTTOM_COUNTRIES_AVG_SCALE.value):
            return _process_by_average_scale_capacity(data, True)
        elif (category == BedsFilter.TOP_COUNTRIES_AVG_ESTIMATE.value):
            return _process_by_average_estimated_capacity(data)
        elif (category == BedsFilter.BOTTOM_COUNTRIES_AVG_ESTIMATE.value):
            return _process_by_average_estimated_capacity(data, True)
        else:
            return _process_general_statistics(data)
    except FileNotFoundError:
        print(f'The file "{BedsFilter.DATA_FILENAME.value}" does not exist')        
        sys.exit('No file, no execution... Stopping!')


def load_bed_records(filter_option, cli_mode = False, sampling = False,
                     send_request = False):
    """
    Retrieves filtered bed records and writes their data on JSON files or sends
    to them to the backend's API according to the specified parameters
    If CLI mode is enabled, the user will be prompted to choose whether a
    request will be sent to the API; otherwise, the sending must be specified
    through the send_request parameter
    """
    records = _filter_beds(filter_option, sampling)

    general_json_list = records[0].to_json() \
        if (filter_option == BedsFilter.GENERAL_STATISTICS.value) \
        else [r.to_json() for r in records[0]]

    types_json_list = [r.to_json() for r in records[1]]

    general_data = json.dumps(general_json_list, indent = 4)
    types_data = json.dumps(types_json_list, indent = 4)

    api_data = [general_data, types_data]

    write_beds_data(general_data, types_data, filter_option)

    if (cli_mode):
        user_input = prompt_user(3)

        if (user_input.lower() == 'yes'):
            api.send_data(api_data, api.BEDS_URL)
    elif (send_request):
        api.send_data(api_data, api.BEDS_URL)