"""Shared request sending logic."""

import logging
from typing import Any, Generic, Literal, TypeVar

from httpx import AsyncClient, Client
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

from whyhow.exceptions import ResponseSuccessValidationError

logger = logging.getLogger(__name__)


class RequestBody(BaseModel):
    """Base class for request body."""

    model_config = ConfigDict(extra="forbid")


class QueryParameters(BaseModel):
    """Base class for request query parameters."""

    model_config = ConfigDict(extra="forbid")


class PathParameters(BaseModel):
    """Base class for request path parameters."""

    model_config = ConfigDict(extra="forbid")


class ResponseBody(BaseModel):
    """Base class for response body."""

    # Allow extra fields in response body to make backend updates easier
    model_config = ConfigDict(extra="ignore")


# Type definitions
Method = Literal["get", "post", "put", "delete", "patch"]
RequestBodyChild = TypeVar("RequestBodyChild", bound=RequestBody)
PathParametersChild = TypeVar("PathParametersChild", bound=PathParameters)
QueryParametersChild = TypeVar("QueryParametersChild", bound=QueryParameters)
ResponseBodyChild = TypeVar("ResponseBodyChild", bound=ResponseBody)


class ResponseBodyError(BaseModel):
    """We assume that the error response will always have a detail field."""

    detail: str

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def check_other_sources(cls, data: Any) -> Any:
        """Check for alternative names for the detail field."""
        alternative_names: list[str] = ["error", "message"]

        if isinstance(data, dict):
            if "detail" in data:
                data["detail"] = str(data["detail"])
                return data

            for name in alternative_names:
                if name in data:
                    data["detail"] = data.pop(name)
                    data["detail"] = str(data["detail"])
                    return data

        return data


class SuccessReturnType(BaseModel, Generic[ResponseBodyChild]):
    """Return type for successful requests."""

    status_code: int
    body: ResponseBodyChild
    headers: dict[str, Any]
    elapsed_seconds: float


class ErrorReturnType(BaseModel):
    """Return type for unsuccessful requests."""

    status_code: int
    body: ResponseBodyError
    headers: dict[str, Any]
    elapsed_seconds: float


def send(
    client: Client,
    method: Method,
    url: str,
    response_body_schema: type[ResponseBodyChild],
    request_body: RequestBodyChild | None = None,
    path_parameters: PathParametersChild | None = None,
    query_parameters: QueryParametersChild | None = None,
) -> SuccessReturnType[ResponseBodyChild] | ErrorReturnType:
    """Send a request to the API and return the response."""
    if path_parameters is not None:
        url = url.format(**path_parameters.model_dump())

    if query_parameters is not None:
        params = query_parameters.model_dump(exclude_none=True)
    else:
        params = None

    body_dict = (
        request_body.model_dump(by_alias=True)
        if request_body is not None
        else None
    )

    logger.debug(f"{method=}, {url=}, {body_dict=}, {params=}")
    full_response = client.request(method, url, json=body_dict, params=params)

    if full_response.status_code == 200:
        try:
            response_body_success = response_body_schema.model_validate(
                full_response.json()
            )
        except ValidationError as e:
            logger.error(f"Response body validation error: {e}")
            raise ResponseSuccessValidationError from e

        return SuccessReturnType(
            status_code=full_response.status_code,
            body=response_body_success,
            headers=dict(full_response.headers),
            elapsed_seconds=full_response.elapsed.total_seconds(),
        )
    else:
        try:
            response_body_error = ResponseBodyError.model_validate(
                full_response.json()
            )
        except ValidationError:
            response_body_error = ResponseBodyError(detail="Unknown error")

        return ErrorReturnType(
            status_code=full_response.status_code,
            body=response_body_error,
            headers=dict(full_response.headers),
            elapsed_seconds=full_response.elapsed.total_seconds(),
        )


async def asend(
    client: AsyncClient,
    method: Method,
    url: str,
    response_body_schema: type[ResponseBodyChild],
    request_body: RequestBodyChild | None = None,
    path_parameters: PathParametersChild | None = None,
    query_parameters: QueryParametersChild | None = None,
) -> SuccessReturnType[ResponseBodyChild] | ErrorReturnType:
    """Send a request to the API and return the response."""
    if path_parameters is not None:
        url = url.format(**path_parameters.model_dump())

    if query_parameters is not None:
        params = query_parameters.model_dump(exclude_none=True)
    else:
        params = None

    body_dict = (
        request_body.model_dump(by_alias=True)
        if request_body is not None
        else None
    )

    logger.debug(f"{method=}, {url=}, {body_dict=}, {params=}")
    full_response = await client.request(
        method, url, json=body_dict, params=params
    )

    if full_response.status_code == 200:
        try:
            response_body_success = response_body_schema.model_validate(
                full_response.json()
            )
        except ValidationError as e:
            logger.error(f"Response body validation error: {e}")
            raise ResponseSuccessValidationError from e

        return SuccessReturnType(
            status_code=full_response.status_code,
            body=response_body_success,
            headers=dict(full_response.headers),
            elapsed_seconds=full_response.elapsed.total_seconds(),
        )
    else:
        try:
            response_body_error = ResponseBodyError.model_validate(
                full_response.json()
            )
        except ValidationError:
            response_body_error = ResponseBodyError(detail="Unknown error")

        return ErrorReturnType(
            status_code=full_response.status_code,
            body=response_body_error,
            headers=dict(full_response.headers),
            elapsed_seconds=full_response.elapsed.total_seconds(),
        )
