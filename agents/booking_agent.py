from datetime import datetime

from models.FlightSearchRequest import FlightSearchRequest
from services.FlightService import FlightService


class BookingAgent:

    def __init__(self):
        self.flight_service = FlightService()

    def find_flights(self, request: FlightSearchRequest) -> list[dict]:

        flights = self.flight_service.search_flights(request)
        matching_flights = []

        for flight in flights:

            if flight["origin"] != request.source:
                continue

            if flight["destination"] != request.destination:
                continue

            flight_date = datetime.fromisoformat(
                flight["departure"]
            ).date()

            requested_date = datetime.strptime(
                request.departure_date,
                "%Y-%m-%d"
            ).date()

            if flight_date != requested_date:
                continue

            if flight["price"] > request.max_amount:
                continue

            if flight["availableSeats"] < request.passengers:
                continue

            if not self._matches_time(flight["departure"], request.preferred_time):
                continue

            matching_flights.append(flight)

        return sorted(matching_flights, key=lambda flight: flight["price"])

    @staticmethod
    def _matches_time(departure: str, preferred_time: str) -> bool:

        if preferred_time == "anytime":
            return True

        hour = datetime.fromisoformat(departure).hour

        if preferred_time == "morning":
            return 5 <= hour < 12

        if preferred_time == "afternoon":
            return 12 <= hour < 17

        if preferred_time == "evening":
            return 17 <= hour < 22

        return True
