# windy-mcp-server

> **Unofficial** MCP server for the [Windy Point Forecast API](https://api.windy.com/point-forecast). This project is not affiliated with or endorsed by Windy.com.

An MCP (Model Context Protocol) server that exposes weather, ocean wave, and air quality forecasts to AI assistants via the Windy Point Forecast API.

## Tools

### `get_weather_forecast`
Fetch atmospheric weather data for any coordinates.

- **Parameters:** temperature, dewpoint, relative humidity, pressure, geopotential height, precipitation (total/snow/convective), wind, wind gusts, cloud cover (low/mid/high), cloud base, visibility, CAPE, precipitation type, weather warnings
- **Models:** GFS, ICON, ICON-EU, ICON-D2, AROME (France, Antilles, Réunion), NAM (CONUS/Hawaii/Alaska), HRRR (CONUS/Alaska), HRDPS
- **Pressure levels:** surface through 150 hPa (14 levels)
- **Temperature units:** Celsius or Kelvin

### `get_wave_forecast`
Fetch ocean wave data for any coastal or open-water coordinates.

- **Parameters:** significant wave height, wind waves, wave power, swell 1 & 2
- **Models:** GFS Wave, ICON Wave, ICON-EU Wave, RDWPS (Canada)

### `get_air_quality_forecast`
Fetch air quality and pollen forecasts for any location.

- **Parameters:** AQI, SO₂, dust, CO, O₃, NO₂, PM10, PM2.5, pollen (alder, birch, grass, mugwort, olive, ragweed)
- **Models:** CAMS (global), CAMS-EU (higher-resolution European data)

## Setup

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/), a [Windy API key](https://api.windy.com/keys)

1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/yourusername/windy-mcp-server.git
   cd windy-mcp-server
   uv sync
   ```

2. Create a `.env` file with your API key:
   ```bash
   cp .env.example .env
   # Edit .env and set WINDY_API_KEY=your_api_key_here
   ```

3. Add to your MCP client config (e.g. `claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "windy": {
         "command": "uv",
         "args": ["run", "python", "server/server.py"],
         "cwd": "/path/to/windy-mcp-server",
         "env": {
           "WINDY_API_KEY": "your_api_key_here"
         }
       }
     }
   }
   ```

## License

MIT
