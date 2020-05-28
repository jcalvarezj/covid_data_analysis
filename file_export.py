"""
This module handles file saving processes
"""

from constants import BedsFilter, MeasuresFilter


def write_to_file(data, filename):
    """
    Writes data on the file with specified name
    """
    try:
        with open(filename, 'w') as export_file:
            export_file.write(data)
        print(f'Wrote the results on {filename}!')
    except OSError as e:
        print(f'Could not write {filename}!')
        print(e)


def write_beds_data(general_json, types_json, filter_index):
    """
    Writes the entered beds json into a file named according to the chosen
    filter
    """
    general_name = BedsFilter(filter_index).name + '_GENERAL'
    types_name = BedsFilter(filter_index).name + '_TYPES'
    general_filename = BedsFilter.EXPORT_FILENAME.value.replace("#", 
                                                                general_name)
    types_filename = BedsFilter.EXPORT_FILENAME.value.replace("#", types_name)
    
    write_to_file(general_json, general_filename)
    write_to_file(types_json, types_filename)


def write_measures_data(filter_index, general_json, types_json = None):
    """
    Writes the entered measures json into a file named according to the chosen
    filter
    """
    general_name = MeasuresFilter(filter_index).name + '_GENERAL'
    general_filename = MeasuresFilter.EXPORT_FILENAME.value.replace("#", 
                                                                general_name)
    write_to_file(general_json, general_filename)
    
    if (types_json):
        types_name = MeasuresFilter(filter_index).name + '_MEASURES'
        types_filename = MeasuresFilter.EXPORT_FILENAME.value.replace("#",
                                                                  types_name)
        write_to_file(types_json, types_filename)