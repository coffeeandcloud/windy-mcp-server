from pydantic import BaseModel, Field

from ..enums import Level, Model, Parameter, TempUnit


class ForecastRequest(BaseModel):
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")
    model: Model = Field(..., description="Forecast model")
    parameters: list[Parameter] = Field(..., min_length=1, description="Requested forecast parameters")
    levels: list[Level] = Field(default=[Level.surface], description="Geopotential altitude levels")
    temp_unit: TempUnit = Field(default=TempUnit.kelvin, description="Unit for temperature values")
