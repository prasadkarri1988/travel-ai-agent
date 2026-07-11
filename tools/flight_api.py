import requests

BASE_URL = "http://localhost:3000"


def get_flights():
    response = requests.get(BASE_URL + "/flights")
    if response.status_code == 200:
        return response.json()
    return []
