from models.FlightSearchRequest import FlightSearchRequest
from agents.booking_agent import BookingAgent


def collect_flight_preferences() -> FlightSearchRequest:
    print("Flight Booking Agent")
    print("--------------------")

    source = input("Enter source airport code (e.g. DFW): ").strip().upper()

    destination = input(
        "Enter destination airport code (e.g. SEA): "
    ).strip().upper()

    departure_date = input(
        "Enter departure date (YYYY-MM-DD): "
    ).strip()

    return_date_input = input(
        "Enter return date (or press Enter for one-way): "
    ).strip()

    max_amount = float(
        input("Enter maximum budget per passenger: ")
    )

    nonstop_input = input(
        "Do you prefer nonstop flights? (yes/no): "
    ).strip().lower()

    preferred_time = input(
        "Preferred departure time (morning/afternoon/evening/anytime): "
    ).strip().lower()

    passengers = int(
        input("Enter number of passengers: ")
    )

    return FlightSearchRequest(
        source=source,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date_input or None,
        max_amount=max_amount,
        nonstop=nonstop_input in ["yes", "y", "true"],
        preferred_time=preferred_time,
        passengers=passengers
    )


def main():
    flight_request = collect_flight_preferences()

    print("\nFlight Request:")
    print(flight_request)

    booking_agent = BookingAgent()

    flights = booking_agent.find_flights(flight_request)

    print("\nMatching Flights:")

    if not flights:
        print("No matching flights found.")
        return

    for flight in flights:
        print(
            f'{flight["airline"]} '
            f'{flight["flightNumber"]} | '
            f'{flight["departure"]} | '
            f'${flight["price"]} | '
            f'Seats: {flight["availableSeats"]}'
        )


if __name__ == "__main__":
    main()