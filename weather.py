import os
import sys
from dotenv import load_dotenv

from typing import Any

import httpx2
from mcp.server import MCPServer

from datetime import datetime, timezone

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

mcp = MCPServer("weather")

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
BIPAD_API_BASE = "https://bipadportal.gov.np/api/v1"

HEADERS = {
    "User-Agent": "weather-mcp-server/1.0 (contact: you@example.com)"
}


async def make_weather_request(url: str) -> dict[str, Any] | None:
    """
    Make a GET request and return parsed JSON, or None on any failure.
    """
    async with httpx2.AsyncClient(headers=HEADERS) as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API request failed for {url}: {e}", file=sys.stderr)
            return None


# implementing tool execution
@mcp.tool()
async def get_weather(latitude: float, longitude: float) -> str:
    """Get current weather from OpenWeather for any location
    using latitude and longitude."""

    if not OPENWEATHER_API_KEY:
        return "Server misconfiguration: OPENWEATHER_API_KEY is not set."

    url = (
        f"{OPENWEATHER_BASE_URL}/weather"
        f"?lat={latitude}"
        f"&lon={longitude}"
        f"&appid={OPENWEATHER_API_KEY}"
        f"&units=metric"
    )

    data = await make_weather_request(url)

    if not data:
        return "Unable to fetch weather data."

    if str(data.get("cod")) != "200":
        return f"OpenWeather error: {data.get('message', 'unknown error')}"

    main = data.get("main", {})
    weather = (data.get("weather") or [{}])[0]
    wind = data.get("wind", {})

    return f"""
Temperature: {main.get('temp', 'N/A')}°C
Feels Like: {main.get('feels_like', 'N/A')}°C
Humidity: {main.get('humidity', 'N/A')}%
Weather: {weather.get('description', 'N/A')}
Wind Speed: {wind.get('speed', 'N/A')} m/s
"""


@mcp.tool()
async def get_alerts(location: str = "Kathmandu") -> str:
    """
    Get active disaster alerts for a specific location in Nepal.
    """

    url = f"{BIPAD_API_BASE}/alert/"
    data = await make_weather_request(url)

    if not data or "results" not in data:
        return "Unable to fetch alerts."

    now = datetime.now(timezone.utc)
    active_alerts = []

    for alert in data["results"]:
        # Check if the alert is still active
        expire_on = alert.get("expireOn")

        if expire_on:
            try:
                expire_time = datetime.fromisoformat(
                    expire_on.replace("Z", "+00:00")
                )

                if expire_time < now:
                    continue

            except ValueError:
                continue

        # Check if the alert is for the requested location
        title = (alert.get("title") or "").lower()
        description = (alert.get("description") or "").lower()
        search_location = location.lower()

        if (
            search_location not in title
            and search_location not in description
        ):
            continue

        active_alerts.append(alert)

    if not active_alerts:
        return f"No active disaster alerts found for {location}."

    formatted_alerts = []

    for alert in active_alerts[:10]:
        formatted_alerts.append(
            f"""
Alert: {alert.get("title", "Unknown")}
Type: {alert.get("referenceType", "Unknown")}
Description: {alert.get("description", "No description available")}
Started: {alert.get("startedOn", "Unknown")}
Expires: {alert.get("expireOn", "Unknown")}
Verified: {alert.get("verified", "Unknown")}
Source: {alert.get("source", "Unknown")}
"""
        )

    return "\n---\n".join(formatted_alerts)


if __name__ == "__main__":
    mcp.run(transport="stdio")