# Travel AI Agent

A Python-based travel flight-search application that demonstrates a gradual transition from a traditional REST API integration to an MCP-based tool architecture.

The project currently collects flight preferences, calls a mock REST API, exposes flight search through an MCP server, connects through an MCP client, filters matching flights, and displays the results.

---

## Project Goal

The long-term goal is to build an Agentic AI travel assistant capable of:

- Understanding natural-language travel requests
- Searching flights, hotels, and rental cars
- Comparing travel options
- Creating itineraries
- Calling external travel APIs through MCP tools
- Using an LLM to decide which tools to call
- Managing multi-step workflows with LangGraph
- Maintaining conversation and trip memory
- Supporting booking and payment workflows

---

# Current Architecture

```text
User
  |
  v
app.py
  |
  v
FlightSearchRequest
  |
  v
BookingAgent
  |
  v
FlightMCPClient
  |
  v
MCP stdio connection
  |
  v
Flight MCP Server
  |
  v
FlightService
  |
  v
Mock REST API
  |
  v
Flight Results
  |
  v
BookingAgent Filtering
  |
  v
Matching Flights
```

---

# Direct API Flow vs MCP Flow

## Previous direct API flow

```text
BookingAgent
  |
  v
FlightService
  |
  v
GET http://localhost:3000/flights
```

The application directly knew:

- REST endpoint
- HTTP method
- Query parameters
- Response format

## Current MCP flow

```text
BookingAgent
  |
  v
FlightMCPClient
  |
  v
search_flights MCP tool
  |
  v
Flight MCP Server
  |
  v
FlightService
  |
  v
Mock REST API
```

The Booking Agent now calls a named capability:

```text
search_flights
```

The MCP server hides the implementation details of the external API.

Today, the MCP server calls the mock REST API.

Later, it can call:

- Amadeus API
- Sabre API
- Travelport API
- Database
- Multiple travel providers

The MCP client does not need major changes if the tool contract remains the same.

---

# Completed Features

- Collect source airport
- Collect destination airport
- Collect departure date
- Collect optional return date
- Collect maximum budget
- Collect nonstop preference
- Collect preferred departure time
- Collect passenger count
- Create a structured `FlightSearchRequest`
- Start a JSON mock REST server
- Call the mock service using Python
- Filter flights by:
  - Source
  - Destination
  - Departure date
  - Maximum budget
  - Available seats
  - Nonstop preference
  - Preferred departure time
- Sort flights by lowest price
- Expose flight search as an MCP tool
- Connect to the MCP server through stdio
- Discover MCP tools
- Call `search_flights` through an MCP client
- Receive flight results through MCP
- Test the MCP server using MCP Inspector
- Test the MCP server using a Python MCP client

---

# Project Structure

```text
travel-ai-agent/
|
├── app.py
├── requirements.txt
├── README.md
|
├── agents/
│   ├── __init__.py
│   └── booking_agent.py
|
├── models/
│   ├── __init__.py
│   └── FlightSearchRequest.py
|
├── services/
│   ├── __init__.py
│   └── flight_service.py
|
├── mcp_server/
│   ├── __init__.py
│   └── flight_mcp_server.py
|
├── mcp_client/
│   ├── __init__.py
│   └── flight_mcp_client.py
|
├── mock-server/
│   └── db.json
|
└── test_mcp_client.py
```

---

# Prerequisites

Install the following:

- Python 3.10 or later
- Node.js
- npm
- PyCharm or another Python IDE
- Git
- MCP Python SDK
- JSON Server

Check installed versions:

```bash
python --version
node --version
npm --version
```

On Windows Git Bash, the `python` command may point to the Microsoft Store alias.

In that case, use the project virtual environment directly:

```bash
./.venv/Scripts/python.exe --version
```

---

# Step 1: Create the Project

Create the project folder:

```bash
mkdir travel-ai-agent
cd travel-ai-agent
```

Or create a new Python project in PyCharm named:

```text
travel-ai-agent
```

---

# Step 2: Create a Virtual Environment

Create the virtual environment:

```bash
python -m venv .venv
```

Windows Command Prompt:

```bash
.venv\Scripts\activate
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Verify the Python executable:

```bash
python --version
```

For Git Bash on Windows:

```bash
./.venv/Scripts/python.exe --version
```

---

# Step 3: Install Dependencies

Install the Python dependencies:

```bash
pip install requests
pip install mcp
```

Or use the virtual environment directly:

```bash
./.venv/Scripts/python.exe -m pip install requests
./.venv/Scripts/python.exe -m pip install mcp
```

Create `requirements.txt`:

```text
requests
mcp
```

You can also generate it:

```bash
pip freeze > requirements.txt
```

---

# Step 4: Create the Flight Request Model

Create:

```text
models/FlightSearchRequest.py
```

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class FlightSearchRequest:
    source: str
    destination: str
    departure_date: str
    return_date: Optional[str]
    max_amount: float
    nonstop: bool
    preferred_time: str
    passengers: int
```

This model stores all flight-search preferences in one structured object.

Example:

```python
FlightSearchRequest(
    source="DFW",
    destination="SEA",
    departure_date="2026-07-20",
    return_date=None,
    max_amount=2000.0,
    nonstop=True,
    preferred_time="morning",
    passengers=4
)
```

---

# Step 5: Create Mock Flight Data

Create:

```text
mock-server/db.json
```

```json
{
  "flights": [
    {
      "id": 1,
      "airline": "Alaska Airlines",
      "flightNumber": "AS322",
      "origin": "DFW",
      "destination": "SEA",
      "departure": "2026-07-20T08:30",
      "arrival": "2026-07-20T11:15",
      "price": 320,
      "availableSeats": 12,
      "nonstop": true
    },
    {
      "id": 2,
      "airline": "Delta",
      "flightNumber": "DL456",
      "origin": "DFW",
      "destination": "SEA",
      "departure": "2026-07-20T10:00",
      "arrival": "2026-07-20T13:05",
      "price": 355,
      "availableSeats": 8,
      "nonstop": true
    },
    {
      "id": 3,
      "airline": "American Airlines",
      "flightNumber": "AA890",
      "origin": "DFW",
      "destination": "SEA",
      "departure": "2026-07-20T15:45",
      "arrival": "2026-07-20T18:40",
      "price": 340,
      "availableSeats": 15,
      "nonstop": false
    }
  ]
}
```

---

# Step 6: Install JSON Server

Install JSON Server globally:

```bash
npm install -g json-server
```

Or install it locally:

```bash
npm install --save-dev json-server
```

---

# Step 7: Start the Mock REST Server

Open a terminal:

```bash
cd mock-server
json-server --watch db.json --port 3000
```

The endpoint will be:

```text
http://localhost:3000/flights
```

Test it in a browser:

```text
http://localhost:3000/flights
```

Expected response:

```json
[
  {
    "id": "1",
    "airline": "Alaska Airlines",
    "flightNumber": "AS322"
  }
]
```

Keep the mock server running while testing the Python application.

---

# Step 8: Create the Flight Service

Create:

```text
services/flight_service.py
```

```python
from typing import Any

import requests

from models.FlightSearchRequest import FlightSearchRequest


class FlightService:

    def __init__(
        self,
        base_url: str = "http://localhost:3000"
    ) -> None:
        self.base_url = base_url

    def search_flights(
        self,
        request: FlightSearchRequest
    ) -> list[dict[str, Any]]:

        url = f"{self.base_url}/flights"

        params = {
            "origin": request.source,
            "destination": request.destination
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if isinstance(data, list):
                return data

            if isinstance(data, dict):
                return data.get("flights", [])

            return []

        except requests.RequestException as error:
            print(f"Flight service call failed: {error}")
            return []
```

## FlightService Responsibility

The `FlightService` is responsible only for communicating with the external REST API.

It should not contain business filtering logic.

```text
FlightService
  |
  v
HTTP GET request
  |
  v
Mock API response
```

---

# Step 9: Create the MCP Server

Create:

```text
mcp_server/flight_mcp_server.py
```

```python
from typing import Any

from mcp.server.fastmcp import FastMCP

from models.FlightSearchRequest import FlightSearchRequest
from services.flight_service import FlightService


mcp = FastMCP("Flight Search MCP Server")

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
        destination: Destination airport code, such as SEA.
        departure_date: Departure date in YYYY-MM-DD format.
        return_date: Optional return date.
        max_amount: Maximum price per passenger.
        nonstop: Whether nonstop flights are required.
        preferred_time: morning, afternoon, evening, or anytime.
        passengers: Number of passengers.
    """

    request = FlightSearchRequest(
        source=source.strip().upper(),
        destination=destination.strip().upper(),
        departure_date=departure_date,
        return_date=return_date,
        max_amount=max_amount,
        nonstop=nonstop,
        preferred_time=preferred_time.strip().lower(),
        passengers=passengers
    )

    return flight_service.search_flights(request)


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## What `@mcp.tool()` Does

This decorator exposes the Python function as an MCP tool:

```text
search_flights
```

The MCP SDK generates:

- Tool name
- Tool description
- Input schema
- Parameter validation
- Tool-call handling

The MCP client can later call:

```python
await session.call_tool(
    "search_flights",
    arguments={
        "source": "DFW",
        "destination": "SEA",
        "departure_date": "2026-07-20"
    }
)
```

---

# Step 10: Start the MCP Server Manually

From the project root:

```bash
python -m mcp_server.flight_mcp_server
```

On Windows Git Bash:

```bash
./.venv/Scripts/python.exe -m mcp_server.flight_mcp_server
```

The terminal may show no response.

That is expected.

The MCP server is running with `stdio` transport and waiting for an MCP client.

```text
MCP Client
  |
  v
stdin
  |
  v
MCP Server
  |
  v
stdout
  |
  v
MCP Client
```

Stop it using:

```text
Ctrl + C
```

Do not add normal `print()` statements to the stdio MCP server because stdout is used for MCP protocol communication.

---

# Step 11: Test with MCP Inspector

From the project root:

```bash
npx @modelcontextprotocol/inspector ./.venv/Scripts/python.exe -m mcp_server.flight_mcp_server
```

The browser-based MCP Inspector should open.

In Inspector:

1. Connect to the server.
2. Open the **Tools** section.
3. Select `search_flights`.
4. Enter:

```json
{
  "source": "DFW",
  "destination": "SEA",
  "departure_date": "2026-07-20",
  "return_date": null,
  "max_amount": 10000,
  "nonstop": true,
  "preferred_time": "anytime",
  "passengers": 4
}
```

5. Click **Run Tool**.

The Inspector sends a request similar to:

```json
{
  "method": "tools/call",
  "params": {
    "name": "search_flights",
    "arguments": {
      "source": "DFW",
      "destination": "SEA",
      "departure_date": "2026-07-20",
      "return_date": null,
      "max_amount": 10000,
      "nonstop": true,
      "preferred_time": "anytime",
      "passengers": 4
    }
  }
}
```

Expected result:

```text
Alaska Airlines
Delta
American Airlines
```

At this stage, the MCP tool mainly retrieves records from the REST API.

Detailed filtering is performed by the `BookingAgent`.

---

# Step 12: Create the Python MCP Client

Create:

```text
mcp_client/flight_mcp_client.py
```

```python
import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

from models.FlightSearchRequest import FlightSearchRequest


class FlightMCPClient:

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parent.parent

        self.server_parameters = StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "mcp_server.flight_mcp_server"
            ],
            cwd=str(project_root)
        )

    async def search_flights(
        self,
        request: FlightSearchRequest
    ) -> list[dict[str, Any]]:

        async with stdio_client(
            self.server_parameters
        ) as (read_stream, write_stream):

            async with ClientSession(
                read_stream,
                write_stream
            ) as session:

                await session.initialize()

                tools_response = await session.list_tools()

                tool_names = [
                    tool.name
                    for tool in tools_response.tools
                ]

                print(f"MCP tools available: {tool_names}")

                if "search_flights" not in tool_names:
                    raise RuntimeError(
                        "search_flights MCP tool was not found."
                    )

                result = await session.call_tool(
                    "search_flights",
                    arguments={
                        "source": request.source,
                        "destination": request.destination,
                        "departure_date": request.departure_date,
                        "return_date": request.return_date,
                        "max_amount": request.max_amount,
                        "nonstop": request.nonstop,
                        "preferred_time": request.preferred_time,
                        "passengers": request.passengers
                    }
                )

                if result.isError:
                    raise RuntimeError(
                        "search_flights MCP tool returned an error."
                    )

                return self._extract_flights(result)

    @staticmethod
    def _extract_flights(
        result: Any
    ) -> list[dict[str, Any]]:

        structured_content = getattr(
            result,
            "structuredContent",
            None
        )

        if structured_content is None:
            structured_content = getattr(
                result,
                "structured_content",
                None
            )

        if isinstance(structured_content, list):
            return structured_content

        if isinstance(structured_content, dict):
            flights = structured_content.get("result")

            if isinstance(flights, list):
                return flights

            flights = structured_content.get("flights")

            if isinstance(flights, list):
                return flights

        for content_item in result.content:
            if not isinstance(content_item, TextContent):
                continue

            parsed_data = json.loads(content_item.text)

            if isinstance(parsed_data, list):
                return parsed_data

            if isinstance(parsed_data, dict):
                flights = parsed_data.get("flights")

                if isinstance(flights, list):
                    return flights

        return []
```

---

# Step 13: Understand the MCP Client

The MCP client performs the following steps:

```text
1. Starts the MCP server process
2. Opens a stdio connection
3. Creates a ClientSession
4. Performs the MCP initialization handshake
5. Discovers available tools
6. Verifies search_flights exists
7. Calls search_flights
8. Receives the MCP result
9. Converts the result into a Python list
```

The server is launched using:

```python
StdioServerParameters(
    command=sys.executable,
    args=[
        "-m",
        "mcp_server.flight_mcp_server"
    ]
)
```

This means the Python MCP client automatically starts the MCP server.

You do not need to manually start the MCP server when running the Python client.

---

# Step 14: Test the Python MCP Client

Create:

```text
test_mcp_client.py
```

```python
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
```

Run the test:

```bash
python test_mcp_client.py
```

On Windows Git Bash:

```bash
./.venv/Scripts/python.exe test_mcp_client.py
```

Expected output:

```text
MCP tools available: ['search_flights']

Flights received through MCP:
Alaska Airlines AS322 | 2026-07-20T08:30 | $320
Delta DL456 | 2026-07-20T10:00 | $355
American Airlines AA890 | 2026-07-20T15:45 | $340
```

---

# Step 15: Create the Booking Agent

Create or update:

```text
agents/booking_agent.py
```

```python
from datetime import datetime
from typing import Any

from mcp_client.flight_mcp_client import FlightMCPClient
from models.FlightSearchRequest import FlightSearchRequest


class BookingAgent:

    def __init__(self) -> None:
        self.flight_mcp_client = FlightMCPClient()

    async def find_flights(
        self,
        request: FlightSearchRequest
    ) -> list[dict[str, Any]]:

        flights = await self.flight_mcp_client.search_flights(
            request
        )

        matching_flights = []

        for flight in flights:

            if flight.get("origin") != request.source:
                continue

            if flight.get("destination") != request.destination:
                continue

            if not self._matches_departure_date(
                flight.get("departure"),
                request.departure_date
            ):
                continue

            if float(
                flight.get("price", 0)
            ) > request.max_amount:
                continue

            if int(
                flight.get("availableSeats", 0)
            ) < request.passengers:
                continue

            if request.nonstop and not flight.get(
                "nonstop",
                False
            ):
                continue

            if not self._matches_preferred_time(
                flight.get("departure"),
                request.preferred_time
            ):
                continue

            matching_flights.append(flight)

        return sorted(
            matching_flights,
            key=lambda flight: flight.get("price", 0)
        )

    @staticmethod
    def _matches_departure_date(
        departure: str | None,
        requested_date: str
    ) -> bool:

        if not departure:
            return False

        flight_date = datetime.fromisoformat(
            departure
        ).date()

        request_date = datetime.strptime(
            requested_date,
            "%Y-%m-%d"
        ).date()

        return flight_date == request_date

    @staticmethod
    def _matches_preferred_time(
        departure: str | None,
        preferred_time: str
    ) -> bool:

        if preferred_time == "anytime":
            return True

        if not departure:
            return False

        departure_hour = datetime.fromisoformat(
            departure
        ).hour

        if preferred_time == "morning":
            return 5 <= departure_hour < 12

        if preferred_time == "afternoon":
            return 12 <= departure_hour < 17

        if preferred_time == "evening":
            return 17 <= departure_hour < 22

        return True
```

---

# Step 16: Booking Agent Responsibilities

The Booking Agent performs business filtering after receiving flights through MCP.

Current rules:

```text
Source matches request
Destination matches request
Departure date matches request
Price is within maximum budget
Available seats are enough
Nonstop condition is satisfied
Preferred time matches
Results are sorted by price
```

The Booking Agent does not know the mock REST API URL.

It communicates only with:

```text
FlightMCPClient
```

---

# Step 17: Create the Main Application

Create or update:

```text
app.py
```

```python
import asyncio

from agents.booking_agent import BookingAgent
from models.FlightSearchRequest import FlightSearchRequest


def collect_flight_preferences() -> FlightSearchRequest:
    print("Flight Booking Agent")
    print("--------------------")

    source = input(
        "Enter source airport code (e.g. DFW): "
    ).strip().upper()

    destination = input(
        "Enter destination airport code (e.g. SEA): "
    ).strip().upper()

    departure_date = input(
        "Enter departure date (YYYY-MM-DD): "
    ).strip()

    return_date_input = input(
        "Enter return date "
        "(or press Enter for one-way): "
    ).strip()

    max_amount = float(
        input(
            "Enter maximum budget per passenger: "
        ).strip()
    )

    nonstop_input = input(
        "Do you prefer nonstop flights? (yes/no): "
    ).strip().lower()

    preferred_time = input(
        "Preferred departure time "
        "(morning/afternoon/evening/anytime): "
    ).strip().lower()

    passengers = int(
        input(
            "Enter number of passengers: "
        ).strip()
    )

    return FlightSearchRequest(
        source=source,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date_input or None,
        max_amount=max_amount,
        nonstop=nonstop_input in [
            "yes",
            "y",
            "true"
        ],
        preferred_time=preferred_time,
        passengers=passengers
    )


async def main() -> None:
    flight_request = collect_flight_preferences()

    print("\nFlight Request:")
    print(flight_request)

    booking_agent = BookingAgent()

    flights = await booking_agent.find_flights(
        flight_request
    )

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
            f'Seats: {flight["availableSeats"]} | '
            f'Nonstop: {flight.get("nonstop", False)}'
        )


if __name__ == "__main__":
    asyncio.run(main())
```

There should be only one `main()` function and one execution block.

```python
if __name__ == "__main__":
    asyncio.run(main())
```

---

# Step 18: Run the Complete Application

## Terminal 1: Start the mock REST server

```bash
cd mock-server
json-server --watch db.json --port 3000
```

Keep this terminal open.

## Terminal 2: Run the Python application

From the project root:

```bash
python app.py
```

On Windows Git Bash:

```bash
./.venv/Scripts/python.exe app.py
```

Do not start the MCP server manually.

The Python MCP client launches the MCP server automatically.

---

# Step 19: Test Input

Use:

```text
Source: DFW
Destination: SEA
Departure date: 2026-07-20
Return date:
Maximum budget: 2000
Nonstop: yes
Preferred time: morning
Passengers: 4
```

Expected request object:

```text
FlightSearchRequest(
    source='DFW',
    destination='SEA',
    departure_date='2026-07-20',
    return_date=None,
    max_amount=2000.0,
    nonstop=True,
    preferred_time='morning',
    passengers=4
)
```

Expected output:

```text
MCP tools available: ['search_flights']

Matching Flights:
Alaska Airlines AS322 |
2026-07-20T08:30 |
$320 |
Seats: 12 |
Nonstop: True

Delta DL456 |
2026-07-20T10:00 |
$355 |
Seats: 8 |
Nonstop: True
```

American Airlines is excluded because:

- It departs in the afternoon
- It is not nonstop

---

# Complete Request Flow

```text
1. User enters flight preferences

2. app.py creates FlightSearchRequest

3. app.py calls BookingAgent

4. BookingAgent calls FlightMCPClient

5. FlightMCPClient starts Flight MCP Server

6. MCP client and server initialize a session

7. MCP client discovers available tools

8. MCP client calls search_flights

9. MCP server executes the search_flights tool

10. MCP tool creates FlightSearchRequest

11. MCP tool calls FlightService

12. FlightService calls:
    GET http://localhost:3000/flights

13. Mock REST API returns JSON

14. FlightService returns flights to MCP server

15. MCP server returns the tool result

16. FlightMCPClient converts the MCP response

17. BookingAgent applies business filters

18. app.py displays matching flights
```

---

# Component Responsibilities

| Component | Responsibility |
|---|---|
| `app.py` | Collect input and coordinate the application |
| `FlightSearchRequest` | Store flight-search preferences |
| `BookingAgent` | Apply flight-search business rules |
| `FlightMCPClient` | Connect to MCP server and call tools |
| `Flight MCP Server` | Expose flight capabilities as MCP tools |
| `FlightService` | Call the external REST API |
| `db.json` | Store mock flight records |
| JSON Server | Expose the mock REST endpoint |
| MCP Inspector | Test MCP tools manually |
| `test_mcp_client.py` | Test MCP client-server integration |

---

# What Has Been Completed

| Feature | Status |
|---|---|
| Flight request model | Completed |
| User preference collection | Completed |
| Mock flight data | Completed |
| JSON REST server | Completed |
| Flight REST service | Completed |
| Booking Agent | Completed |
| Flight filtering | Completed |
| Price sorting | Completed |
| MCP SDK installation | Completed |
| MCP server | Completed |
| MCP tool registration | Completed |
| MCP Inspector testing | Completed |
| MCP Python client | Completed |
| MCP tool discovery | Completed |
| MCP tool invocation | Completed |
| MCP response handling | Completed |
| End-to-end MCP client test | Completed |
| BookingAgent MCP integration | Current integration step |
| LLM tool selection | Not started |
| LangGraph workflow | Not started |
| Real Amadeus API | Not started |

---

# Current Milestone

The project currently demonstrates:

```text
Traditional Python Application
+
REST API Integration
+
MCP Server
+
MCP Client
+
MCP Tool Discovery
+
MCP Tool Invocation
+
Business Rule Filtering
```

The MCP layer is working, but the application does not yet contain an LLM.

The application currently calls:

```python
session.call_tool(
    "search_flights",
    arguments={...}
)
```

directly from Python code.

---

# Is This Fully Agentic AI Yet?

Not yet.

The current application is:

```text
Structured workflow
+
MCP tools
```

A true agentic flow will add an LLM that decides:

```text
The user wants flights.

I should call the search_flights tool.

I should inspect the result.

I may need another tool.

I should produce a final recommendation.
```

Future flow:

```text
User natural-language request
  |
  v
LLM Agent
  |
  v
Tool-selection decision
  |
  v
MCP Client
  |
  v
MCP Server
  |
  v
Flight Tool
  |
  v
Flight API
```

---

# Next Phase

The next phase is LLM and workflow integration.

Recommended next steps:

```text
1. Create a shared TravelState model

2. Add natural-language user input

3. Connect an LLM

4. Give the LLM access to MCP tool definitions

5. Allow the LLM to select search_flights

6. Execute the MCP tool

7. Return the tool result to the LLM

8. Generate a user-friendly recommendation

9. Add LangGraph workflow orchestration

10. Add error and retry handling
```

---

# Future Architecture

```text
User
  |
  v
Travel Assistant UI
  |
  v
LLM Agent
  |
  v
LangGraph Workflow
  |
  +----------------------+
  |                      |
  v                      v
Planner Agent       Booking Agent
                         |
                         v
                    MCP Client
                         |
                         v
                    MCP Server
        +----------------+----------------+
        |                |                |
        v                v                v
  Flight Tool       Hotel Tool       Weather Tool
        |                |                |
        v                v                v
  Amadeus API       Hotel API       Weather API
```

---

# Future Enhancements

- LLM integration
- Natural-language travel input
- LangGraph
- Shared travel state
- Conversation memory
- Hotel-search agent
- Rental-car agent
- Weather tool
- Currency-conversion tool
- Trip-cost calculator
- Amadeus API integration
- Provider fallback
- Retry logic
- Input validation
- Logging
- Unit tests
- Integration tests
- FastAPI backend
- React frontend
- Authentication
- Database persistence
- Docker
- AWS deployment
- Monitoring
- API security
- Secrets management

---

# Learning Outcomes

This project demonstrates:

- Python project organization
- Dataclasses
- Request object pattern
- Service-layer design
- Agent-layer design
- REST API integration
- JSON response processing
- Business-rule separation
- Async Python
- MCP host-client-server architecture
- MCP stdio transport
- MCP initialization
- MCP tool discovery
- MCP tool invocation
- MCP tool result handling
- External API abstraction
- Migration from direct API calls to MCP tools

---

# Summary

The project has progressed through the following architecture stages.

## Stage 1

```text
User
  |
  v
app.py
  |
  v
Mock data
```

## Stage 2

```text
User
  |
  v
BookingAgent
  |
  v
FlightService
  |
  v
Mock REST API
```

## Stage 3

```text
User
  |
  v
BookingAgent
  |
  v
FlightMCPClient
  |
  v
Flight MCP Server
  |
  v
FlightService
  |
  v
Mock REST API
```

## Next stage

```text
User
  |
  v
LLM Agent
  |
  v
MCP tool decision
  |
  v
FlightMCPClient
  |
  v
Flight MCP Server
  |
  v
Flight API
```