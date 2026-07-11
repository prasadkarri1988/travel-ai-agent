import requests

from models.FlightSearchRequest import FlightSearchRequest


class FlightService:
    def __init__(self):
        self.baseURL = "http://localhost:3000";

    def search_flights(self, request: FlightSearchRequest) -> list[dict]:
        url = f"{self.baseURL}/flights"
        try:
            response = requests.get(url)
            response.raise_for_status()
            response = response.json()
            print(response)
            return response;
        except Exception as e:
            print(e)
            return []
