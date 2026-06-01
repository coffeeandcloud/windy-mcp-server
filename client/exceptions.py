class WindyAPIError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class WindyNoContentError(WindyAPIError):
    """204 — the selected model has none of the requested parameters."""


class WindyBadRequestError(WindyAPIError):
    """400 — invalid request body."""


class WindyServerError(WindyAPIError):
    """500 — backend failure."""
