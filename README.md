# Travel AI Agent

## Project Goal

Build an enterprise-grade Agentic AI Travel Booking System using Python, MCP (Model Context Protocol), LangGraph, and
LLMs.

The application will eventually allow users to search and book flights, hotels, rental cars, and complete payments using
multiple AI agents.

---

# Overall Roadmap

```
Phase 1  → Planner Agent ✅
Phase 2  → Booking Agent ✅
Phase 3  → MCP Integration
Phase 4  → LangGraph Workflow
Phase 5  → Memory
Phase 6  → Hotel Agent
Phase 7  → Rental Car Agent
Phase 8  → Payment Agent
Phase 9  → Amadeus Real API
Phase 10 → React UI
Phase 11 → Production Deployment
```

---

# Phase 1 - Planner Agent ✅

## Objective

Collect all travel requirements from the user.

### User Input

- Source Airport
- Destination Airport
- Departure Date
- Return Date
- Maximum Budget
- Preferred Time
- Nonstop Preference
- Number of Passengers

Example

```
DFW
SEA
2026-07-20

2000
Morning
Yes
4
```

---

## FlightSearchRequest Model

Created a model called

```
FlightSearchRequest
```

Purpose

Store all user preferences in one object.

Example

```
FlightSearchRequest

source

destination

departure_date

return_date

max_amount

nonstop

preferred_time

passengers
```

This object is passed to the Booking Agent.

---

# Phase 2 - Mock Flight API ✅

## Objective

Create a fake airline service.

Created

```
mock-server/db.json
```

Example

```
{
   "flights":[
      ...
   ]
}
```

Started mock server

```
json-server --watch db.json --port 3000
```

Endpoint

```
GET http://localhost:3000/flights
```

Purpose

Instead of calling a real airline API, the application calls this mock server.

---

# Phase 3 - Flight Service ✅

Created

```
services/flight_service.py
```

Responsibility

Only communicate with the external API.

Flow

```
FlightService

↓

GET /flights

↓

Receive JSON Response
```

No business logic is written here.

---

# Phase 4 - Booking Agent ✅

Created

```
agents/booking_agent.py
```

Responsibility

Receive FlightSearchRequest

↓

Call FlightService

↓

Receive Flight List

↓

Apply Business Rules

↓

Return Matching Flights

---

## Business Rules

Current filtering

✓ Source

✓ Destination

✓ Departure Date

✓ Budget

✓ Passenger Count

✓ Preferred Time

(Nonstop filtering will be enabled after adding the nonstop field in mock data.)

---

## Sorting

Flights are sorted by

```
Lowest Price
```

---

# Phase 5 - Main Application ✅

Created

```
app.py
```

Responsibilities

Collect user input

↓

Create FlightSearchRequest

↓

Call BookingAgent

↓

Display Matching Flights

---

# Current Flow

```
User

↓

Planner Agent

↓

FlightSearchRequest

↓

Booking Agent

↓

Flight Service

↓

Mock Flight API

↓

Matching Flights
```

---

# Testing

Input

```
Source : DFW

Destination : SEA

Departure : 2026-07-20

Budget : 2000

Passengers : 4

Morning

Nonstop
```

Output

```
Alaska Airlines

Delta Airlines
```

American Airlines is filtered because it departs in the afternoon.

---

# Project Structure

```
travel-ai-agent/

app.py

agents/
    booking_agent.py

models/
    FlightSearchRequest.py

services/
    flight_service.py

mock-server/
    db.json

requirements.txt

README.md
```

---

# What We Learned

- Project Structure
- Layered Architecture
- Dataclass Model
- REST API Calling
- JSON Server
- Business Logic Separation
- Service Layer
- Agent Layer
- Request Object Pattern

---

# Current Architecture

```
             User
               │
               ▼
       Planner Agent
               │
               ▼
    FlightSearchRequest
               │
               ▼
       Booking Agent
               │
               ▼
       Flight Service
               │
               ▼
      Mock Flight API
               │
               ▼
       Matching Flights
```

---

# Progress

| Phase                | Status      |
|----------------------|-------------|
| Planner Agent        | ✅ Completed |
| Flight Request Model | ✅ Completed |
| Mock Flight API      | ✅ Completed |
| Flight Service       | ✅ Completed |
| Booking Agent        | ✅ Completed |
| Flight Filtering     | ✅ Completed |
| End-to-End Flow      | ✅ Completed |

Current Progress

```
35%
```

---

# Next Step

Integrate MCP (Model Context Protocol)

Future Architecture

```
Planner Agent

↓

Booking Agent

↓

MCP Client

↓

MCP Server

↓

Flight Service

↓

Mock Flight API
```

After MCP

```
Mock Flight API

↓

Amadeus Flight API
```

---

# Future Enhancements

- MCP Server
- MCP Client
- LangGraph
- LLM Integration
- Memory
- Hotel Agent
- Rental Car Agent
- Payment Agent
- Real Amadeus API
- React Frontend
- Docker
- AWS Deployment

---

# End Goal

Build a production-ready enterprise Agentic AI Travel Booking Platform capable of autonomously planning, searching,
comparing, and booking travel using multiple AI agents.