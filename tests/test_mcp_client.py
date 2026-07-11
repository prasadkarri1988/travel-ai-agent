import asyncio

from mcp_client.flight_mcp_client import FlightMCPClient
from models.FlightSearchRequest import FlightSearchRequest


async def main() -> None:
    request = FlightSearchRequest(
        source="DFW",
        destination="SEA",
        departure_date="2026-07-20",
        return_date=None,
        max_amount=10000,
        nonstop=True,
        preferred_time="anytime",
        passengers=4
    )

    client = FlightMCPClient()

    flights = await client.search_flights(request)

    print("\nFlights received through MCP:")

    if not flights:
        print("No flights returned.")
        return

    for flight in flights:
        print(
            f'{flight["airline"]} '
            f'{flight["flightNumber"]} | '
            f'{flight["departure"]} | '
            f'${flight["price"]}'
        )


if __name__ == "__main__":
    asyncio.run(main())