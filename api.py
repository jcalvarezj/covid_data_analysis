"""
This module allows communication with the backend's API through POST requests
with information of the datasets
"""

import json
import grequests
from constants import BEDS_URL, MEASURES_URL, HEADERS


def handle_exception(request, exception):
    """
    Exception handler callback function
    """
    print('Could not perform the request due to a problem:')
    print(exception)


def send_data(json_data_list, endpoint):
    """
    Attempts to send a POST request to the Bed endpoint
    """
    pending_requests = []
        
    for json_struct in json_data_list:
        pending_requests.append(grequests.post(endpoint, data = json_struct,
                                               headers = HEADERS))        

    print('Going to send the requests')

    responses = grequests.map(pending_requests, 
                              exception_handler = handle_exception)

    print('Requests sent')

    for index, response in enumerate(responses):
        if (response.status_code == 201):
            print(f'SUCCESS! Response #{index}:')
            print(response.json())
        else:
            print(f'Problem with the request. Response #{index}:')
            print(response.status_code)
            print(response.json())