import os
from dotenv import load_dotenv

# Load values from the .env file
load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434/v1"
)

OLLAMA_API_KEY = os.getenv(
    "OLLAMA_API_KEY",
    "ollama"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama3.2:latest"
)

# Amadeus flight API configuration
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")