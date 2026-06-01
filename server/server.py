import os
import sys
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Literal

from dotenv import load_dotenv
from fastmcp import Context, FastMCP

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from client import (
    ForecastRequest,
    Level,
    Model,
    Parameter,
    TempUnit,
    WindyBadRequestError,
    WindyClient,
    WindyNoContentError,
    WindyServerError,
)

load_dotenv()

# --- Type aliases for tool parameter schemas ---

WeatherModel = Literal[
    "gfs",
    "icon",
    "iconEu",
    "iconD2",
    "arome",
    "aromeAntilles",
    "aromeFrance",
    "aromeReunion",
    "namConus",
    "namHawaii",
    "namAlaska",
    "hrrrConus",
    "hrrrAlaska",
    "canHrdps",
]

WaveModel = Literal["gfsWave", "iconWave", "iconEuWave", "canRdwpsWave"]

AirQualityModel = Literal["cams", "camsEu"]

WeatherParameter = Literal[
    "temp",
    "dewpoint",
    "rh",
    "pressure",
    "gh",
    "precip",
    "snowPrecip",
    "convPrecip",
    "wind",
    "windGust",
    "lclouds",
    "mclouds",
    "hclouds",
    "cbase",
    "visibility",
    "cape",
    "ptype",
    "weatherWarnings",
]

WaveParameter = Literal["waves", "windWaves", "wavesPower", "swell1", "swell2"]

AirQualityParameter = Literal[
    "aqi",
    "so2sm",
    "dustsm",
    "cosc",
    "go3",
    "no2",
    "pm10",
    "pm2p5",
    "pollenAlder",
    "pollenBirch",
    "pollenGrass",
    "pollenMugwort",
    "pollenOlive",
    "pollenRagweed",
]

PressureLevel = Literal[
    "surface",
    "1000h",
    "950h",
    "925h",
    "900h",
    "850h",
    "800h",
    "700h",
    "600h",
    "500h",
    "400h",
    "300h",
    "200h",
    "150h",
]

TemperatureUnit = Literal["celsius", "kelvin"]


# --- Lifespan: manage WindyClient lifecycle ---


@asynccontextmanager
async def lifespan(server: FastMCP):
    api_key = os.environ.get("WINDY_API_KEY")
    if not api_key:
        raise RuntimeError("WINDY_API_KEY environment variable is required")
    client = WindyClient(api_key=api_key)
    try:
        yield {"client": client}
    finally:
        await client.close()


mcp = FastMCP("Windy Point Forecast", lifespan=lifespan)


# --- Helpers ---


def _fmt_ts(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).strftime("%Y-%m-%d %H:%M UTC")


def _build_response(response) -> dict:
    return {
        "timestamps_utc": [_fmt_ts(ts) for ts in response.timestamps],
        "series": [
            {
                "parameter_level": s.parameter_level,
                "unit": s.unit,
                "values": s.values,
            }
            for s in response.series
        ],
    }


async def _call_forecast(
    client: WindyClient, request: ForecastRequest, model_name: str
) -> dict:
    try:
        response = await client.get_forecast(request)
        return _build_response(response)
    except WindyNoContentError as e:
        raise ValueError(
            f"No data available for model '{model_name}' with the requested"
            " parameters at this location"
        ) from e
    except WindyBadRequestError as e:
        raise ValueError(f"Invalid request: {e}") from e
    except WindyServerError as e:
        raise RuntimeError(f"Windy API server error: {e}") from e


# --- Tools ---


@mcp.tool
async def get_weather_forecast(
    lat: float,
    lon: float,
    parameters: list[WeatherParameter],
    ctx: Context,
    model: WeatherModel = "gfs",
    levels: list[PressureLevel] | None = None,
    temp_unit: TemperatureUnit = "celsius",
) -> dict:
    """Get a weather forecast for a specific location from the Windy point forecast API.

    Returns forecast time series for the requested parameters. Only the parameters you
    explicitly list are fetched — request only what you need.

    Args:
        lat: Latitude in decimal degrees (-90 to 90).
        lon: Longitude in decimal degrees (-180 to 180).
        parameters: Weather parameters to fetch. Choose from temperature, wind,
            precipitation, clouds, visibility, and atmospheric instability indicators.
        ctx: Injected server context.
        model: Forecast model to use. Defaults to GFS (global coverage).
        levels: Pressure levels for vertical atmosphere data. Defaults to surface only.
            Use hPa values (e.g. "850h", "500h") for upper-atmosphere queries.
        temp_unit: Unit for temperature values. Defaults to celsius.
    """
    client: WindyClient = ctx.lifespan_context["client"]
    resolved_levels = [Level(lv) for lv in levels] if levels else [Level.surface]
    request = ForecastRequest(
        lat=lat,
        lon=lon,
        model=Model(model),
        parameters=[Parameter(p) for p in parameters],
        levels=resolved_levels,
        temp_unit=TempUnit.celsius if temp_unit == "celsius" else TempUnit.kelvin,
    )
    return await _call_forecast(client, request, model)


@mcp.tool
async def get_wave_forecast(
    lat: float,
    lon: float,
    parameters: list[WaveParameter],
    ctx: Context,
    model: WaveModel = "gfsWave",
) -> dict:
    """Get an ocean wave forecast for a location from the Windy point forecast API.

    Returns forecast time series for the requested wave parameters. Only the parameters
    you explicitly list are fetched — request only what you need.

    Args:
        lat: Latitude in decimal degrees (-90 to 90).
        lon: Longitude in decimal degrees (-180 to 180).
        parameters: Wave parameters to fetch
            (wave height, wind waves, swell, wave power).
        ctx: Injected server context.
        model: Wave forecast model to use. Defaults to GFS Wave (global coverage).
    """
    client: WindyClient = ctx.lifespan_context["client"]
    request = ForecastRequest(
        lat=lat,
        lon=lon,
        model=Model(model),
        parameters=[Parameter(p) for p in parameters],
        levels=[Level.surface],
        temp_unit=TempUnit.kelvin,
    )
    return await _call_forecast(client, request, model)


@mcp.tool
async def get_air_quality_forecast(
    lat: float,
    lon: float,
    parameters: list[AirQualityParameter],
    ctx: Context,
    model: AirQualityModel = "cams",
) -> dict:
    """Get an air quality and pollen forecast for a location from the Windy API.

    Returns forecast time series for the requested air quality or pollen parameters.
    Only the parameters you explicitly list are fetched — request only what you need.

    Args:
        lat: Latitude in decimal degrees (-90 to 90).
        lon: Longitude in decimal degrees (-180 to 180).
        parameters: Air quality or pollen parameters to fetch
            (AQI, particulates, gases, pollen types).
        ctx: Injected server context.
        model: Air quality model to use. Defaults to CAMS (global Copernicus service).
            Use "camsEu" for higher-resolution European data.
    """
    client: WindyClient = ctx.lifespan_context["client"]
    request = ForecastRequest(
        lat=lat,
        lon=lon,
        model=Model(model),
        parameters=[Parameter(p) for p in parameters],
        levels=[Level.surface],
        temp_unit=TempUnit.kelvin,
    )
    return await _call_forecast(client, request, model)


if __name__ == "__main__":
    mcp.run()
