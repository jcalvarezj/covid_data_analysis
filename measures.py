"""
This module contains functions for processing the measures/restrictions dataset
"""

import api
import json
import pycountry
import pandas as pd
from datetime import datetime
from commons import prompt_user
from urllib.parse import urlparse
from file_export import write_measures_data
from constants import MeasuresFilter, TOP_N, REMAINING_ISO_CODES
from datatypes import (MeasuresGroupData, MeasuresData, MeasuresGeneralData,
                       MeasuresDetailData)


def _get_series_count(series):
    raw_count = dict(series.value_counts().sort_index())
    return [{"keywords": keyword, "count": int(count)}
            for keyword, count in raw_count.items()]


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


def _get_separated_keywords(original_keywords_series):
    """
    Returns a Series with all independent keywords from the keywords Series
    (separated from comma lists)
    """
    keywords_list = []

    [[keywords_list.append(key) for key in record.split(', ')]
     for record in original_keywords_series.values.tolist()]

    return pd.Series(keywords_list)


def _pack_records(country_gb, limit = None):
    """
    From a filtered grouped dataframe, return a list with MeasuresGroupData and
    MeasuresData lists
    Precondition: The dataset has been normalized and contains the 'Code',
    'Source Domain' and 'Keywords Count' columns
    """
    measure_records = []
    measure_data = []

    for country_name, country_group in list(country_gb)[:limit]:
        iso_code = ""

        if (type(country_name) is tuple):
            iso_code = country_name[1].lower()
        else:
            iso_code = country_name.lower()

        separated_keywords = _get_separated_keywords(country_group['Keywords'])
        keywords_count = _get_series_count(separated_keywords)
        keywords_total = int(country_group['Keywords Count'].values[0])
        records_total = int(country_group['Records Count'].values[0])
        raw_sources_count = dict(country_group['Source Domain'].value_counts())

        sources_count = [{"sources": source, "count": int(count)}
                         for source, count in raw_sources_count.items()]

        new_record = MeasuresGroupData(code = iso_code,
                                       keywords_count = keywords_count,
                                       keywords_total = keywords_total,
                                       keywords_records_total = records_total,
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

            new_data = MeasuresData(code = iso_code,
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
    if (pd.notna(url)):
        return urlparse(url).netloc
    else:
        return pd.NA


def _count_different_keywords(keywords_series):
    """
    Returns the count of all unique separated keywords 
    """
    return len(_get_separated_keywords(keywords_series).unique())


def _count_keywords_records(keywords_series):
    """
    Returns the count of all unique separated keywords 
    """
    return len(_get_separated_keywords(keywords_series))


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
    data['Keywords Count'] = data.groupby('Code')['Keywords'] \
                                     .transform(_count_different_keywords)
    data['Records Count'] = data.groupby('Code')['Keywords'] \
                                     .transform(_count_keywords_records)


def _process_without_filter(data):
    """
    Returns the basic structure for the whole dataset without filter
    Precondition: the dataset has been normalized and it has the 'Code' column
    """
    country_gb = data.groupby('Code')
    return _pack_records(country_gb)


def _process_by_measure_count(data, ascending = False):
    """
    Returns the basic structure for the dataset, filtering by the N top or
    bottom countries with a number 
    Precondition: the dataset has been normalized and it has the 'Code' and
    'Keywords Count' columns
    """
    country_gb = data.groupby('Code')
    sorted_data = data.sort_values(['Keywords Count'], ascending = ascending)
    country_gb = sorted_data.groupby(['Keywords Count','Code'], sort = False)

    return _pack_records(country_gb, TOP_N)


def _process_by_records_count(data, ascending = False):
    """
    Returns the basic structure for the dataset, filtering by the N top or
    bottom countries with a number 
    Precondition: the dataset has been normalized and it has the 'Code' and
    'Keywords Count' columns
    """
    country_gb = data.groupby('Code')
    sorted_data = data.sort_values(['Records Count'], ascending = ascending)
    country_gb = sorted_data.groupby(['Records Count','Code'], sort = False)

    return _pack_records(country_gb, TOP_N)


def _process_general_information(data):
    """
    Returns the dataset's general information
    Precondition: the dataset has been normalized and it has the 'Code',
    'Keywords Count', and 'Source Domain' columns
    """
    counts = data[['Code', 'Keywords Count']]
    unique_counts = counts[~counts.duplicated()]
    m_counts = dict(zip(unique_counts['Code'],
                        unique_counts['Keywords Count']))

    separated_keywords = _get_separated_keywords(data['Keywords'])
    keywords_count = _get_series_count(separated_keywords)

    sources_count = _get_series_count(data['Source Domain'])

    general_data = MeasuresGeneralData(countries_measures_count = m_counts,
                                       all_keywords_count = keywords_count,
                                       all_sources_count = sources_count)

    return [general_data] # TODO: Including detail data - To be Determined


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
        elif (category == MeasuresFilter.TOP_COUNTRIES_MEASURE_COUNT.value):
            return _process_by_measure_count(data)
        elif (category == MeasuresFilter.BOTTOM_COUNTRIES_MEASURE_COUNT.value):
            return _process_by_measure_count(data, ascending = True)
        elif (category == MeasuresFilter.TOP_COUNTRIES_RECORDS_COUNT.value):
            return _process_by_records_count(data)
        elif (category == MeasuresFilter.BOTTOM_COUNTRIES_RECORDS_COUNT.value):
            return _process_by_records_count(data, ascending = True)
        else:
            return _process_general_information(data)
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
    
    if (filter_option != MeasuresFilter.GENERAL_STATISTICS.value):
        general_json_list = [r.to_json() for r in records[0]]

        types_json_list = [r.to_json() for r in records[1]]

        general_data = json.dumps(general_json_list, indent = 4)
        types_data = json.dumps(types_json_list, indent = 4)

        api_data = [general_data, types_data]

        write_measures_data(filter_option, general_data, types_data)

        if (cli_mode):
            user_input = prompt_user(3)
            answer = user_input.lower() == 'yes'

            if (answer):
                api.send_data(api_data, api.MEASURES_URL)
        elif (send_request):
            api.send_data(api_data, api.MEASURES_URL)
    else:
        general_json_list = records[0].to_json()
        general_data = json.dumps(general_json_list, indent = 4)
        api_data = [general_data]
        write_measures_data(filter_index = filter_option, 
                            general_json = general_data)

        if (cli_mode):
            user_input = prompt_user(3)
            answer = user_input.lower() == 'yes'

            if (answer):
                api.send_data(api_data, api.MEASURES_URL)
        elif (send_request):
            api.send_data(api_data, api.MEASURES_URL)