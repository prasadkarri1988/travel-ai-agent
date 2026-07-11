from typing import Any

from mcp.server.fastmcp import FastMCP

from models.FlightSearchRequest import FlightSearchRequest
from services.FlightService import FlightService

# Creates the MCP server
mcp = FastMCP("Flight Search MCP Server")

# Existing REST service that calls the JSON mock server
flight_service = FlightService()


@mcp.tool()
def search_flights(
        source: str,
        destination: str,
        departure_date: str,
        return_date: str | None = None,
        max_amount: float = 10000.0,
        nonstop: bool = False,
        preferred_time: str = "anytime",
        passengers: int = 1
) -> list[dict[str, Any]]:
    """
    Search available flights.

    Args:
        source: Departure airport code, such as DFW.
        destination: Arrival airport code, such as SEA.
        departure_date: Travel date in YYYY-MM-DD format.
        return_date: Optional return date for round-trip travel.
        max_amount: Maximum price per passenger.
        nonstop: Whether the passenger prefers nonstop flights.
        preferred_time: morning, afternoon, evening, or anytime.
        passengers: Number of passengers.
    """

    flight_request = FlightSearchRequest(
        source=source.strip().upper(),
        destination=destination.strip().upper(),
        departure_date=departure_date,
        return_date=return_date,
        max_amount=max_amount,
        nonstop=nonstop,
        preferred_time=preferred_time.strip().lower(),
        passengers=passengers
    )

    flights = flight_service.search_flights(flight_request)

    return flights


if __name__ == "__main__":
    mcp.run(transport="stdio")
