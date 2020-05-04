import grequests
import json


URL = 'https://jsonplaceholder.typicode.com/posts'
data = [
    {
        "code": "be",
        "lat": 50.836,
        "lng": 111.12,
        "bedsTotal": 888
    }, 
    {
        "code": "co",
        "lat": 10.836,
        "lng": 1.12,
        "bedsTotal": 10
    }, 
    {
        "code": "ze",
        "lat": 56,
        "lng": 1.12,
        "bedsTotal": 80
    }
]
headers = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}


def sendBedsData(records):
    requests = []

    for r in records:
        requests.append(
            grequests.post(URL, data = json.dumps(r), headers = headers)
        )

    responses = grequests.map(requests)

    for r in responses:
        if (r.status_code == 201):
            print(r.status_code)
            print(r.json())
        else:
            print("There was a problem with the request")
            print(r.status_code)
            print(r.json())


if __name__ == "__main__":
    sendBedsData(data)