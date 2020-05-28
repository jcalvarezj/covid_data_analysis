"""
This module stores the global constants used by the application
"""

from enum import Enum


class BedsFilter(Enum):
    """
    Enum that provides constant integers to describe category filters for the
    beds dataset and strings for input and output file names
    """
    NUMBER_PERCENT_COUNTRY_NORMAL = 1
    TOP_COUNTRIES_SCALE = 2
    BOTTOM_COUNTRIES_SCALE = 3
    TOP_COUNTRIES_ESTIMATE = 4
    BOTTOM_COUNTRIES_ESTIMATE = 5
    TOP_COUNTRIES_AVG_SCALE = 6
    BOTTOM_COUNTRIES_AVG_SCALE = 7
    TOP_COUNTRIES_AVG_ESTIMATE = 8
    BOTTOM_COUNTRIES_AVG_ESTIMATE = 9
    GENERAL_STATISTICS = 10
    DATA_FILENAME = './data/hospital_beds.csv'
    EXPORT_FILENAME = './export/beds/#.json'
    SAMPLE_RECORDS = 24


class MeasuresFilter(Enum):
    """
    Enum that provides constant integers to describe category filters for the
    measures and restrictions dataset, as well as strings for input and output
    file names
    """
    GENERAL_COUNTRY_INFORMATION = 1
    TOP_COUNTRIES_MEASURE_COUNT = 2
    BOTTOM_COUNTRIES_MEASURE_COUNT = 3
    TOP_COUNTRIES_RECORDS_COUNT = 4
    BOTTOM_COUNTRIES_RECORDS_COUNT = 5
    GENERAL_STATISTICS = 6
    ## TODO: Add more filter options
    DATA_FILENAME = './data/measures.csv'
    EXPORT_FILENAME = './export/measures/#.json'
    SAMPLE_RECORDS = 30


TOP_N = 10
BED_FILTERS = [
    'Number and percentage of beds per type, by country (scale)',
    f'Top {TOP_N} countries with highest bed capacity (scale)',
    f'Top {TOP_N} countries with lowest bed capacity (scale)',
    f'Top {TOP_N} countries with highest bed capacity (estimated)',
    f'Top {TOP_N} countries with lowest bed capacity (estimated)',
    f'Top {TOP_N} countries with highest average bed capacity (scale)',
    f'Top {TOP_N} countries with lowest average bed capacity (scale)',
    f'Top {TOP_N} countries with highest average bed capacity (estimated)',
    f'Top {TOP_N} countries with lowest average bed capacity (estimated)',
    'General dataset statistics'
]
MEASURE_FILTERS = [
    'General measures by country',
    f'Top {TOP_N} contries with highest count of different measures',
    f'Top {TOP_N} contries with lowest count of different measures',
    f'Top {TOP_N} contries with highest count of measure records',
    f'Top {TOP_N} contries with lowest count of measure records',
    'General dataset statistics'
]
MENU = [
    '''Please enter the desired option:

    (1) Global bed capacity
    (2) Measures and restrictions by country
    (0) Exit program''',
    '''\nBeds dataset chosen. What filter would you like to apply?\n''',
    '''\nMeasures dataset chosen. What filter would you like to apply?\n''',
    '''\nDo you want to send the results to the API?
    Type "yes" if you want to; otherwise, hit the Enter (Return) key\n'''
]
REMAINING_ISO_CODES = {
    'Vietnam': 'VN',
    'South Korea': 'KR',
    'Taiwan': 'TW',
    'Macau': 'MO',
    'European Union': 'EU',
    'North Korea': 'KP',
    'Moldova': 'MD',
    'Macedonia': 'MK',
    'Vatican City': 'VA',
    'Kosovo': 'XK',
    'Iran': 'IR',
    'Russia': 'RU',
    'Palestine': 'PS'
}
BEDS_URL = 'https://api-covid-pi.now.sh/bed'
#MEASURES_URL = 'https://api-covid-pi.now.sh/xmeasurex' # TODO: Update endpoint
MEASURES_URL = 'https://jsonplaceholder.typicode.com/posts' #TODO
HEADERS = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}