import requests
import json


URL = 'https://api-covid-pi.now.sh/bed'
REQUEST_HEADERS = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}


def sendBedsData(jsonData):
    try:
        response = requests.post(URL, data = jsonData, headers = REQUEST_HEADERS)

        if (response.status_code == 201):
            print('SUCCESS!')
            print(response.json())
        else:
            print("There was a problem with the request")
            print(response.status_code)
            print(response.json())
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('Could not perform the request due to an error:')
        print(e)