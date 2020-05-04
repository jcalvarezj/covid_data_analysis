import requests
import json


URL = 'https://jsonplaceholder.typicode.com/posts'
data = [{
    "code": "ad",
    "lat": 42.5,
    "lng": 1.5,
    "bedsTotal": 2.571,
    "bedsAverage": 1.2855,
    "populationAverage": 84105.0,
    "estimatedBedsTotal": 1.2855,
    "estimatedBedsAverage": None,
    "bedType": [
        {
            "icu": 0.071,
            "percentage": 2.761571373006612,
            "population": 83747,
            "estimatedForPopulation": 594.6036999999999,
            "source": "icm-journal",
            "sourceUrl": "https://link.springer.com/article/10.1007/s00134-012-2627-8",
            "year": 2011
        },
        {
            "total": 2.5,
            "percentage": 97.23842862699338,
            "population": 84463,
            "estimatedForPopulation": 21115.75,
            "source": "wdi",
            "sourceUrl": "https://data.worldbank.org/indicator/SH.MED.BEDS.ZS",
            "year": 2009
        }
    ]
}, {
    "code": "ae",
    "lat": 24.0,
    "lng": 54.0,
    "bedsTotal": 1.2,
    "bedsAverage": 1.2,
    "populationAverage": 9197910.0,
    "estimatedBedsTotal": 1.2,
    "estimatedBedsAverage": None,
    "bedType": [
        {
            "total": 1.2,
            "percentage": 100.0,
            "population": 9197910,
            "estimatedForPopulation": 1103749.2,
            "source": "wdi",
            "sourceUrl": "https://data.worldbank.org/indicator/SH.MED.BEDS.ZS",
            "year": 2013
        }
    ]
}]
request_headers = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}


def sendBedsData(records):
    stuff = json.dumps(records, indent = 4)
    print(stuff)
    response = requests.post(URL, data = stuff,
                             headers = request_headers)

    if (response.status_code == 201):
        print('SUCCESS!')
        print(response.json())
    else:
        print("There was a problem with the request")
        print(r.status_code)
        print(r.json())
    

if __name__ == "__main__":
    sendBedsData(data)