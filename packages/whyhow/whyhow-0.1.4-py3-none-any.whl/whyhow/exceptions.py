"""Collection of all custom exceptions for the package."""

from typing import Any


# Status code derived exceptions
class StatusCodeError(Exception):
    """Base class for all exceptions that correspond to a status code."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        correlation_id: str | None,
        additional_details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
        self.correlation_id = correlation_id
        self.additional_details = (
            additional_details if (additional_details is not None) else {}
        )

    def __str__(self) -> str:
        """Return a string representation of the exception."""
        additional_details_str = ", ".join(
            f"{k}: {v}" for k, v in self.additional_details.items()
        )
        if not additional_details_str:
            return (
                f"[Status Code: {self.status_code}] {self.detail} | "
                f"Correlation ID: {self.correlation_id}"
            )
        else:
            return (
                f"[Status Code: {self.status_code}] {self.detail} | "
                f"Correlation ID: {self.correlation_id} | "
                f"Additional Details: {additional_details_str}"
            )


class BadRequestError(StatusCodeError):
    """Raised when a request is malformed.

    Corresponds to a 400 status code.
    """


class AuthenticationError(StatusCodeError):
    """Raised when authentication fails.

    Corresponds to a 401 status code.
    """


class NotFoundError(StatusCodeError):
    """Raised when a resource is not found.

    Corresponds to a 404 status code.
    """


class ValidationError(StatusCodeError):
    """Raised when a request is invalid.

    Corresponds to a 422 status code
    """


class RateLimitError(StatusCodeError):
    """Raised when the rate limit is exceeded.

    Corresponds to a 429 status code.
    """


class InternalServerError(StatusCodeError):
    """Raised when the server encounters an error.

    Corresponds to a 500 status code.
    """


# Miscellaneous exceptions
class ResponseSuccessValidationError(Exception):
    """Raised when a successful response is not parsable.

    This signals that the SDK and the API are out of sync.
    """
