"""Requests for the workspaces endpoints."""

from typing import Literal

from httpx import AsyncClient, Client

from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.workspaces.schemas import (
    CreateWorkspaceRequestBody,
    CreateWorkspaceResponseBody,
    DeleteWorkspacePathParameters,
    DeleteWorkspaceResponseBody,
    GetAllWorkspacesQueryParameters,
    GetAllWorkspacesResponseBody,
    GetWorkspacePathParameters,
    GetWorkspaceResponseBody,
    UpdateWorkspacePathParameters,
    UpdateWorkspaceRequestBody,
    UpdateWorkspaceResponseBody,
    WorkspaceNameRaw,
)


# sync functions
def get_workspace(
    client: Client,
    workspace_id: str,
) -> SuccessReturnType[GetWorkspaceResponseBody] | ErrorReturnType:
    """Get a workspace by its ID."""
    url = "/workspaces/{workspace_id}"
    path_parameters = GetWorkspacePathParameters(workspace_id=workspace_id)

    return send(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetWorkspaceResponseBody,
    )


def get_all_workspaces(
    client: Client,
    skip: int | None = None,
    limit: int | None = None,
    name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllWorkspacesResponseBody] | ErrorReturnType:
    """Get all workspaces."""
    url = "/workspaces"
    query_parameters = GetAllWorkspacesQueryParameters(
        skip=skip, limit=limit, name=name, order=order
    )

    return send(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllWorkspacesResponseBody,
    )


def create_workspace(
    client: Client,
    name: str,
) -> SuccessReturnType[CreateWorkspaceResponseBody] | ErrorReturnType:
    """Create a workspace."""
    url = "/workspaces"
    body = CreateWorkspaceRequestBody(name=name)

    return send(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateWorkspaceResponseBody,
    )


def update_workspace(
    client: Client,
    workspace_id: str,
    name: str,
) -> SuccessReturnType[UpdateWorkspaceResponseBody] | ErrorReturnType:
    """Update a workspace by its ID."""
    url = "/workspaces/{workspace_id}"
    path_parameters = UpdateWorkspacePathParameters(workspace_id=workspace_id)
    body = UpdateWorkspaceRequestBody(name=WorkspaceNameRaw(root=name))

    return send(
        client=client,
        url=url,
        method="put",
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=UpdateWorkspaceResponseBody,
    )


def delete_workspace(
    client: Client,
    workspace_id: str,
) -> SuccessReturnType[DeleteWorkspaceResponseBody] | ErrorReturnType:
    """Delete a workspace by its ID."""
    url = "/workspaces/{workspace_id}"
    path_parameters = DeleteWorkspacePathParameters(workspace_id=workspace_id)

    return send(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteWorkspaceResponseBody,
    )


# async functions
async def aget_workspace(
    client: AsyncClient,
    workspace_id: str,
) -> SuccessReturnType[GetWorkspaceResponseBody] | ErrorReturnType:
    """Get a workspace by its ID."""
    url = "/workspaces/{workspace_id}"
    path_parameters = GetWorkspacePathParameters(workspace_id=workspace_id)

    return await asend(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetWorkspaceResponseBody,
    )


async def aget_all_workspaces(
    client: AsyncClient,
    skip: int | None = None,
    limit: int | None = None,
    name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllWorkspacesResponseBody] | ErrorReturnType:
    """Get all workspaces."""
    url = "/workspaces"
    query_parameters = GetAllWorkspacesQueryParameters(
        skip=skip, limit=limit, name=name, order=order
    )

    return await asend(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllWorkspacesResponseBody,
    )


async def acreate_workspace(
    client: AsyncClient,
    name: str,
) -> SuccessReturnType[CreateWorkspaceResponseBody] | ErrorReturnType:
    """Create a workspace."""
    url = "/workspaces"
    body = CreateWorkspaceRequestBody(name=name)

    return await asend(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateWorkspaceResponseBody,
    )


async def aupdate_workspace(
    client: AsyncClient,
    workspace_id: str,
    name: str,
) -> SuccessReturnType[UpdateWorkspaceResponseBody] | ErrorReturnType:
    """Update a workspace by its ID."""
    url = "/workspaces/{workspace_id}"
    path_parameters = UpdateWorkspacePathParameters(workspace_id=workspace_id)
    body = UpdateWorkspaceRequestBody(name=WorkspaceNameRaw(root=name))

    return await asend(
        client=client,
        url=url,
        method="put",
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=UpdateWorkspaceResponseBody,
    )


async def adelete_workspace(
    client: AsyncClient,
    workspace_id: str,
) -> SuccessReturnType[DeleteWorkspaceResponseBody] | ErrorReturnType:
    """Delete a workspace by its ID."""
    url = "/workspaces/{workspace_id}"
    path_parameters = DeleteWorkspacePathParameters(workspace_id=workspace_id)

    return await asend(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteWorkspaceResponseBody,
    )
