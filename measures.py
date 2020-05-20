"""
This module contains functions for processing the measures/restrictions dataset
"""

import api
import json
from datetime import datetime
import pycountry
import pandas as pd
from numpy import nan
from commons import prompt_user
from urllib.parse import urlparse
from file_export import write_measures_data
from datatypes import MeasuresGroupData, MeasuresData
from constants import MeasuresFilter, TOP_N, REMAINING_ISO_CODES


def _get_from_nan_col(value, is_list):
    """
    Returne None if the value is nan; otherwise, returns the value
    """
    result = None
    if (pd.notna(value)):
        if (is_list):
            result = value.split(', ')
        else:
            result = value
    return result


def _pack_records(country_gb):
    """
    From a filtered grouped dataframe, return a list with MeasuresGroupData and
    MeasuresData lists
    Precondition: The dataset has been normalized and contains the 'Code' and
    'Source Domain' columns
    """
    measure_records = []
    measure_data = []

    for country_name, country_group in country_gb:
        keywords_list = []

        [[keywords_list.append(key) for key in record.split(', ')]
         for record in country_group['Keywords'].values.tolist()]
        
        keywords_series = pd.Series(keywords_list)
        raw_keywords_count = dict(keywords_series.value_counts().sort_index())

        keywords_count = {keyword: int(count) for keyword, count
                          in raw_keywords_count.items()}

        raw_sources_count = dict(country_group['Source Domain'].value_counts())

        sources_count = {source: int(count) for source, count
                         in raw_sources_count.items()}

        new_record = MeasuresGroupData(code = country_name.lower(),
                                       keywords_count = keywords_count,
                                       sources_count = sources_count)

        measure_records.append(new_record)

        for index, row in country_group.iterrows():
            n_date_start = row['Date Start']
            date_start = None
            if (pd.notna(n_date_start)):
                dt_start = datetime.strptime(n_date_start, '%b %d, %Y')
                date_start = dt_start.strftime('%Y-%m-%d')

            n_date_end = row['Date end intended']
            date_end = None
            if (pd.notna(n_date_end)):
                dt_end = datetime.strptime(n_date_end, '%b %d, %Y')
                date_end = dt_end.strftime('%Y-%m-%d')

            description = _get_from_nan_col(
                              row['Description of measure implemented'], False)

            raw_quantity = _get_from_nan_col(row['Quantity'], False)
            quantity = None
            if (raw_quantity):
                quantity = int(raw_quantity)
                              
            exceptions = _get_from_nan_col(row['Exceptions'], True)

            keywords = row['Keywords'].split(', ')

            implementing_cities = _get_from_nan_col(row['Implementing City'],
                                                    True)
            implementing_states = _get_from_nan_col(
                                      row['Implementing State/Province'], True)
            target_countries = _get_from_nan_col(row['Target country'], True)
            target_regions = _get_from_nan_col(row['Target region'], True)

            source = _get_from_nan_col(row['Source'], False)

            new_data = MeasuresData(code = country_name.lower(),
                                    date_start = date_start,
                                    date_end = date_end,
                                    description = description,
                                    keywords = keywords,
                                    exceptions = exceptions,
                                    quantity = quantity,
                                    implementing_cities = implementing_cities,
                                    implementing_states = implementing_states,
                                    target_countries = target_countries,
                                    target_regions = target_regions,
                                    source = source)

            measure_data.append(new_data)

    return [measure_records, measure_data]


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


def _get_url_domain(url):
    """
    Retrieves the domain from the input URL
    """
    if(pd.notna(url)):
        return urlparse(url).netloc
    else:
        return nan


def _transform_measures_dataset(data):
    """
    Deletes records with empty values on the 'Keywords' and 'Country' columns,
    adds the 'Code' column with the ISO 3166 - alpha 2 code of the country
    names in 'Country', and adds the 'Source Domain' column with the domain of
    the urls in 'Source'
    """
    data.dropna(subset = ['Keywords', 'Country'], inplace = True)
    data['Code'] = data['Country'].apply(_country_to_iso)
    data['Source Domain'] = data['Source'].apply(_get_url_domain)


def _process_without_filter(data):
    """
    Returns the basic structure of the whole dataset without filter
    Precondition: the dataset has been normalized and it has the 'Code' column
    """
    country_gb = data.groupby('Code')
    return(_pack_records(country_gb))


def _filter_measures(category, sampling = False):
    """
    Returns the dataset (pandas.core.frame.DataFrame) filtered by the input
    filter category. If the sampling parameter is set to true, only a number
    of records will be taken from the dataset according to the value of the
    MeasuresFilter.SAMPLE_RECORDS constant
    The returned structure is a list with two elements:
    [0]: General structure for country information
    [1]: Information for restrictions
    """
    try:
        data = pd.read_csv(MeasuresFilter.DATA_FILENAME.value)

        if sampling:
            data = data.head(MeasuresFilter.SAMPLE_RECORDS.value)

        _transform_measures_dataset(data)
        
        if (category == MeasuresFilter.GENERAL_COUNTRY_INFORMATION.value):
            return _process_without_filter(data)
        else:
            raise Exception("Not implemented yet")
    except FileNotFoundError:
        print(f'The file "{BedsFilter.DATA_FILENAME.value}" does not exist')
        sys.exit('No file, no execution... Stopping!')


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
    records = _filter_measures(filter_option, sampling)
    
    general_json_list = records[0].to_json() \
        if (filter_option == MeasuresFilter.GENERAL_STATISTICS.value) \
        else [r.to_json() for r in records[0]]

    types_json_list = [r.to_json() for r in records[1]]

    general_data = json.dumps(general_json_list, indent = 4)
    types_data = json.dumps(types_json_list, indent = 4)

    api_data = [general_data, types_data]

    write_measures_data(general_data, types_data, filter_option)

    if (cli_mode):
        user_input = prompt_user(3)
        answer = user_input.lower() == 'yes'

        if (answer):
            api.send_data(api_data, api.MEASURES_URL)
    elif (send_request):
        api.send_data(api_data, api.MEASURES_URL)