"""Chunk requests."""

from typing import Literal

from httpx import AsyncClient, Client

from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.chunks.schemas import (
    AddChunksToWorkspacePathParameters,
    AddChunksToWorkspaceRequestBody,
    AddChunksToWorkspaceResponseBody,
    GetAllChunksQueryParameters,
    GetAllChunksResponseBody,
    GetChunkPathParameters,
    GetChunkQueryParameters,
    GetChunkResponseBody,
)


# sync functions
def get_chunk(
    client: Client,
    chunk_id: str,
    include_embeddings: bool | None = None,
) -> SuccessReturnType[GetChunkResponseBody] | ErrorReturnType:
    """Get chunk by ID."""
    url = f"/chunks/{chunk_id}"
    path_parameters = GetChunkPathParameters(
        chunk_id=chunk_id,
    )
    query_parameters = GetChunkQueryParameters(
        include_embeddings=include_embeddings,
    )
    return send(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        query_parameters=query_parameters,
        response_body_schema=GetChunkResponseBody,
    )


def get_all_chunks(
    client: Client,
    skip: int | None = None,
    limit: int | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    document_id: str | None = None,
    document_filename: str | None = None,
    include_embeddings: bool | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllChunksResponseBody] | ErrorReturnType:
    """Get all chunks."""
    url = "/chunks"
    query_parameters = GetAllChunksQueryParameters(
        skip=skip,
        limit=limit,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        document_id=document_id,
        document_filename=document_filename,
        include_embeddings=include_embeddings,
        order=order,
    )

    return send(
        client=client,
        method="get",
        url=url,
        query_parameters=query_parameters,
        response_body_schema=GetAllChunksResponseBody,
    )


def add_chunks_to_workspace(
    client: Client,
    workspace_id: str,
    body: AddChunksToWorkspaceRequestBody,
) -> SuccessReturnType[AddChunksToWorkspaceResponseBody] | ErrorReturnType:
    """Add chunks to workspace."""
    url = "/chunks/{workspace_id}"
    path_parameters = AddChunksToWorkspacePathParameters(
        workspace_id=workspace_id,
    )

    return send(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=AddChunksToWorkspaceResponseBody,
    )


# async functions
async def aget_chunk(
    client: AsyncClient,
    chunk_id: str,
    include_embeddings: bool | None = None,
) -> SuccessReturnType[GetChunkResponseBody] | ErrorReturnType:
    """Get chunk by ID."""
    url = f"/chunks/{chunk_id}"
    path_parameters = GetChunkPathParameters(
        chunk_id=chunk_id,
    )
    query_parameters = GetChunkQueryParameters(
        include_embeddings=include_embeddings,
    )
    return await asend(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        query_parameters=query_parameters,
        response_body_schema=GetChunkResponseBody,
    )


async def aget_all_chunks(
    client: AsyncClient,
    skip: int | None = None,
    limit: int | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    document_id: str | None = None,
    document_filename: str | None = None,
    include_embeddings: bool | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllChunksResponseBody] | ErrorReturnType:
    """Get all chunks."""
    url = "/chunks"
    query_parameters = GetAllChunksQueryParameters(
        skip=skip,
        limit=limit,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        document_id=document_id,
        document_filename=document_filename,
        include_embeddings=include_embeddings,
        order=order,
    )

    return await asend(
        client=client,
        method="get",
        url=url,
        query_parameters=query_parameters,
        response_body_schema=GetAllChunksResponseBody,
    )


async def aadd_chunks_to_workspace(
    client: AsyncClient,
    workspace_id: str,
    body: AddChunksToWorkspaceRequestBody,
) -> SuccessReturnType[AddChunksToWorkspaceResponseBody] | ErrorReturnType:
    """Add chunks to workspace."""
    url = "/chunks/{workspace_id}"
    path_parameters = AddChunksToWorkspacePathParameters(
        workspace_id=workspace_id,
    )

    return await asend(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=AddChunksToWorkspaceResponseBody,
    )
