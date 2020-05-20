"""
This module allows communication with the backend's API through POST requests
with information of the datasets
"""

import grequests
import json


BEDS_URL = 'https://api-covid-pi.now.sh/bed'
MEASURES_URL = 'https://api-covid-pi.now.sh/xmeasurex' # TODO: Update endpoint
HEADERS = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}


def handle_exception(request, exception):
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