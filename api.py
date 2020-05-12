import grequests
import json


URL = 'https://api-covid-pi.now.sh/bed'
HEADERS = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}


def handle_exception(request, exception):
    print('Could not perform the request due to a problem:')
    print(exception)


def sendBedsData(json_data_list):
    """
    Attempts to send a POST request to the Bed endpoint
    """
    pending_requests = []
        
    for record in json_data_list:
        pending_requests.append(grequests.post(URL, data = record,
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