"""Requests for the schemas endpoints."""

from typing import Literal

from httpx import AsyncClient, Client

from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.schemas.schemas import (
    CreateSchemaRequestBody,
    CreateSchemaResponseBody,
    DeleteSchemaPathParameters,
    DeleteSchemaResponseBody,
    GenerateSchemaRequestBody,
    GenerateSchemaResponseBody,
    GetAllSchemasQueryParameters,
    GetAllSchemasResponseBody,
    GetSchemaPathParameters,
    GetSchemaResponseBody,
)


# sync functions
def get_schema(
    client: Client,
    schema_id: str,
) -> SuccessReturnType[GetSchemaResponseBody] | ErrorReturnType:
    """Get the schema."""
    url = f"/schemas/{schema_id}"
    path_parameters = GetSchemaPathParameters(schema_id=schema_id)

    return send(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetSchemaResponseBody,
    )


def get_all_schemas(
    client: Client,
    skip: int | None = None,
    limit: int | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllSchemasResponseBody] | ErrorReturnType:
    """Get all schemas."""
    url = "/schemas"
    query_parameters = GetAllSchemasQueryParameters(
        skip=skip,
        limit=limit,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        order=order,
    )

    return send(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllSchemasResponseBody,
    )


def create_schema(
    client: Client,
    body: CreateSchemaRequestBody,
) -> SuccessReturnType[CreateSchemaResponseBody] | ErrorReturnType:
    """Create a schema."""
    url = "/schemas"

    return send(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateSchemaResponseBody,
    )


def delete_schema(
    client: Client,
    schema_id: str,
) -> SuccessReturnType[DeleteSchemaResponseBody] | ErrorReturnType:
    """Delete the schema."""
    url = f"/schemas/{schema_id}"
    path_parameters = DeleteSchemaPathParameters(schema_id=schema_id)

    return send(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteSchemaResponseBody,
    )


def generate_schema(
    client: Client,
    questions: list[str],
) -> SuccessReturnType[GenerateSchemaResponseBody] | ErrorReturnType:
    """Generate a schema."""
    url = "/schemas/generate"
    workspace = 24 * "a"  # temporary hack
    body = GenerateSchemaRequestBody(workspace=workspace, questions=questions)

    return send(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=GenerateSchemaResponseBody,
    )


# async functions
async def aget_schema(
    client: AsyncClient,
    schema_id: str,
) -> SuccessReturnType[GetSchemaResponseBody] | ErrorReturnType:
    """Get the schema."""
    url = f"/schemas/{schema_id}"
    path_parameters = GetSchemaPathParameters(schema_id=schema_id)

    return await asend(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetSchemaResponseBody,
    )


async def aget_all_schemas(
    client: AsyncClient,
    skip: int | None = None,
    limit: int | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllSchemasResponseBody] | ErrorReturnType:
    """Get all schemas."""
    url = "/schemas"
    query_parameters = GetAllSchemasQueryParameters(
        skip=skip,
        limit=limit,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        order=order,
    )

    return await asend(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllSchemasResponseBody,
    )


async def acreate_schema(
    client: AsyncClient,
    body: CreateSchemaRequestBody,
) -> SuccessReturnType[CreateSchemaResponseBody] | ErrorReturnType:
    """Create a schema."""
    url = "/schemas"

    return await asend(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateSchemaResponseBody,
    )


async def adelete_schema(
    client: AsyncClient,
    schema_id: str,
) -> SuccessReturnType[DeleteSchemaResponseBody] | ErrorReturnType:
    """Delete the schema."""
    url = f"/schemas/{schema_id}"
    path_parameters = DeleteSchemaPathParameters(schema_id=schema_id)

    return await asend(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteSchemaResponseBody,
    )


async def agenerate_schema(
    client: AsyncClient,
    questions: list[str],
) -> SuccessReturnType[GenerateSchemaResponseBody] | ErrorReturnType:
    """Generate a schema."""
    url = "/schemas/generate"
    workspace = 24 * "a"  # temporary hack
    body = GenerateSchemaRequestBody(workspace=workspace, questions=questions)

    return await asend(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=GenerateSchemaResponseBody,
    )
