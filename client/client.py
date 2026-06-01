from types import TracebackType

import httpx

from .exceptions import WindyAPIError, WindyBadRequestError, WindyNoContentError, WindyServerError
from .models.request import ForecastRequest
from .models.response import ForecastResponse


class WindyClient:
    BASE_URL = "https://api.windy.com/api/point-forecast/v2"

    def __init__(self, api_key: str, timeout: float = 30.0) -> None:
        self._api_key = api_key
        self._timeout = timeout
        self._http: httpx.AsyncClient | None = None

    async def _get_http(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=self._timeout)
        return self._http

    async def get_forecast(self, request: ForecastRequest) -> ForecastResponse:
        payload = request.model_dump(mode="json", by_alias=False)
        # Serialize enum values to their string representation
        payload["model"] = request.model.value
        payload["parameters"] = [p.value for p in request.parameters]
        payload["levels"] = [l.value for l in request.levels]
        payload["key"] = self._api_key

        http = await self._get_http()
        response = await http.post(self.BASE_URL, json=payload)

        if response.status_code == 204:
            raise WindyNoContentError(
                "The selected model has no data for the requested parameters.",
                status_code=204,
            )
        if response.status_code == 400:
            raise WindyBadRequestError(
                f"Bad request: {response.text}",
                status_code=400,
            )
        if response.status_code == 500:
            raise WindyServerError(
                "Windy API internal server error.",
                status_code=500,
            )
        if response.status_code != 200:
            raise WindyAPIError(
                f"Unexpected status {response.status_code}: {response.text}",
                status_code=response.status_code,
            )

        return ForecastResponse.from_raw(response.json(), temp_unit=request.temp_unit)

    async def close(self) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    async def __aenter__(self) -> "WindyClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
