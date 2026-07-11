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

                # MCP client-server handshake
                await session.initialize()

                # Optional check: discover tools exposed by server
                tools_response = await session.list_tools()

                tool_names = [
                    tool.name
                    for tool in tools_response.tools
                ]

                print(f"MCP tools available: {tool_names}")

                if "search_flights" not in tool_names:
                    raise RuntimeError(
                        "search_flights tool was not found."
                    )

                # Call the MCP tool
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
                        "MCP search_flights tool returned an error."
                    )

                return self._extract_flights(result)

    @staticmethod
    def _extract_flights(
        result: Any
    ) -> list[dict[str, Any]]:

        # Newer SDK responses may provide structured content
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

        # Fallback: MCP may return JSON inside TextContent
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