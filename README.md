# Nepal Weather MCP Server

A simple MCP server that provides weather data and disaster alerts for Nepal, built on top of the [Model Context Protocol](https://modelcontextprotocol.io/).

## Tools

### `get_weather(latitude, longitude)`
Fetches current weather (temperature, feels-like, humidity, conditions, wind speed) from the OpenWeather API for any coordinates.

### `get_alerts(location="Kathmandu")`
Fetches disaster alerts from Nepal's [BIPAD Portal](https://bipadportal.gov.np/) API, filtered by location name and active status.

## Status

**Working:**
- `get_weather` - tested and returning correct live data.

**Not fully working / untested:**
- `get_alerts` - runs without crashing and returns correctly formatted output, but hasn't been confirmed to surface real, current alerts. The BIPAD `/alert/` endpoint doesn't sort results by date and its `count` field is unreliable, so relevant alerts may not appear even when the location filter and expiry logic are correct. Needs more testing against live data before it can be trusted.

## Setup

1. Install dependencies: `uv sync` 
2. Set `OPENWEATHER_API_KEY` in a `.env` file
3. Run: `python server.py` (or `uv run python server.py`)

The server uses stdio transport and is meant to be launched by an MCP client (e.g. Claude Desktop), not run interactively.

## Known limitations

- `get_alerts` location matching is a simple substring match on alert title/description — it won't catch alerts tagged only by ward ID or a different location field.
- No caching or rate-limit handling for either API.
