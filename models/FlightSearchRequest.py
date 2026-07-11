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
    passengers: int = 1