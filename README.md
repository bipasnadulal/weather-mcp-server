# Nepal Weather MCP Server

A simple MCP server that provides **live weather data and disaster alerts for Nepal**, built using the [Model Context Protocol](https://modelcontextprotocol.io/).

## Tools

### `get_weather(latitude, longitude)`

Fetches current weather data from the OpenWeather API for any coordinates, including:

* Temperature
* Feels-like temperature
* Humidity
* Weather conditions
* Wind speed

### `get_alerts(location="Kathmandu")`

Fetches disaster alerts from Nepal's [BIPAD Portal](https://bipadportal.gov.np/) API.

The tool filters alerts based on:

* Location
* Active/valid alert status

## Status

**Working:**

* `get_weather` - tested and returning live weather data correctly.
* `get_alerts` - tested and returning formatted disaster alert information from the BIPAD API.

The server has been tested with the MCP stdio transport and is designed to be used by an MCP client such as Claude Desktop.

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 3. Run the server

```bash
python weather.py
```

or:

```bash
uv run python weather.py
```

The server uses **stdio transport** and is intended to be launched and managed by an MCP client such as Claude Desktop.

## Example Usage

Once connected to an MCP client, you can ask questions such as:

```text
What's the current weather in Kathmandu?
```

or:

```text
Are there any active disaster alerts in Kathmandu?
```

The MCP client can then call the appropriate tool:

```text
get_weather
get_alerts
```

## Known Limitations

* `get_alerts` uses location-based matching, so alerts that are associated only with a ward ID or a different location field may not be matched.
* The BIPAD `/alert/` endpoint does not reliably sort results by date, so the returned alerts may not always be ordered from newest to oldest.
* The project currently focuses on Nepal-specific weather and disaster information.

## Tech Stack

* Python
* Model Context Protocol (MCP)
* OpenWeather API
* BIPAD Portal API
* `uv`
* `python-dotenv`

## Project Purpose

This project was built to explore **MCP server development**, API integration, and connecting external real-world data sources to AI assistants through MCP tools.
