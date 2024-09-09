"""Base classes for API schemas."""

from abc import ABC
from typing import cast

from httpx import AsyncClient, Client
from pydantic import BaseModel, ConfigDict

from whyhow.exceptions import (
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from whyhow.raw.base import (
    ErrorReturnType,
    ResponseBodyChild,
    SuccessReturnType,
)


class Resource(BaseModel, ABC):
    """Base class for sync resource schemas."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: Client


class AsyncResource(BaseModel, ABC):
    """Base class for async resource schemas."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: AsyncClient


def validate(
    raw: SuccessReturnType[ResponseBodyChild] | ErrorReturnType,
) -> ResponseBodyChild:
    """Convert a raw response to a resource."""
    if raw.status_code == 200:
        raw = cast(SuccessReturnType[ResponseBodyChild], raw)
        return raw.body

    raw = cast(ErrorReturnType, raw)
    correlation_id = raw.headers.get("x-request-id")

    if raw.status_code == 400:
        raise BadRequestError(
            detail=raw.body.detail,
            status_code=raw.status_code,
            correlation_id=correlation_id,
        )

    elif raw.status_code == 401:
        raise AuthenticationError(
            detail=raw.body.detail,
            status_code=raw.status_code,
            correlation_id=correlation_id,
        )

    elif raw.status_code == 404:
        raise NotFoundError(
            detail=raw.body.detail,
            status_code=raw.status_code,
            correlation_id=correlation_id,
        )

    elif raw.status_code == 422:
        raise ValidationError(
            detail=raw.body.detail,
            status_code=raw.status_code,
            correlation_id=correlation_id,
        )

    elif raw.status_code == 429:
        additional_details = {
            "x-ratelimit-limit": raw.headers.get("x-ratelimit-limit"),
            "x-ratelimit-remaining": raw.headers.get("x-ratelimit-remaining"),
            "x-ratelimit-reset": raw.headers.get("x-ratelimit-reset"),
        }
        raise RateLimitError(
            detail=raw.body.detail,
            status_code=raw.status_code,
            correlation_id=correlation_id,
            additional_details=additional_details,
        )

    elif raw.status_code == 500:
        raise InternalServerError(
            detail=raw.body.detail,
            status_code=raw.status_code,
            correlation_id=correlation_id,
        )
    else:
        raise ValueError(f"Unhandled status code {raw.status_code}")
