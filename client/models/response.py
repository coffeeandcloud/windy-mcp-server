from pydantic import BaseModel

from ..enums import TempUnit


class ForecastSeries(BaseModel):
    parameter_level: str
    unit: str | None
    values: list[float | None]


class ForecastResponse(BaseModel):
    timestamps: list[int]
    series: list[ForecastSeries]

    @classmethod
    def from_raw(
        cls, data: dict, temp_unit: TempUnit = TempUnit.kelvin
    ) -> "ForecastResponse":
        timestamps: list[int] = data["ts"]
        units: dict[str, str | None] = data.get("units", {})

        reserved = {"ts", "units"}
        series = []
        for key, value in data.items():
            if key in reserved or not isinstance(value, list):
                continue
            unit = units.get(key)
            values: list[float | None] = value
            if temp_unit == TempUnit.celsius and unit == TempUnit.kelvin.value:
                values = [v - 273.15 if v is not None else None for v in values]
                unit = TempUnit.celsius.value
            series.append(ForecastSeries(parameter_level=key, unit=unit, values=values))

        return cls(timestamps=timestamps, series=series)
