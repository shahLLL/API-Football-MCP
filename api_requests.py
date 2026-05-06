import httpx
import os
from typing import Any
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Define Constants
USER_AGENT = "footy-app/1.0"
API_KEY = os.environ.get("API_KEY")

# API Request Call
async def make_api_request(url: str) -> dict[str, Any] | None:
    """Make a request to API-Football with proper error handling."""
    headers = {"User-Agent": USER_AGENT, 'x-apisports-key': API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
