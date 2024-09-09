"""Collection of Pydantic models for the workspace routers."""

from typing import Literal

from whyhow.raw.autogen import (
    Name3,
    WorkspaceCreate,
    WorkspaceOut,
    WorkspacesResponse,
    WorkspaceUpdate,
)
from whyhow.raw.base import (
    PathParameters,
    QueryParameters,
    RequestBody,
    ResponseBody,
)

# Auxiliary models
WorkspaceNameRaw = Name3
WorkspaceRaw = WorkspaceOut


# GET /workspaces/{workspace_id}
class GetWorkspacePathParameters(PathParameters):
    """Path parameters for the get workspace endpoint."""

    workspace_id: str


class GetWorkspaceResponseBody(ResponseBody, WorkspacesResponse):
    """Response body for the get workspace endpoint."""


# GET /workspaces
class GetAllWorkspacesQueryParameters(QueryParameters):
    """Query parameters for the get all workspaces endpoint."""

    skip: int | None
    limit: int | None
    name: str | None
    order: Literal["ascending", "descending"] | None


class GetAllWorkspacesResponseBody(ResponseBody, WorkspacesResponse):
    """Response body for the get all workspaces endpoint."""


# POST /workspaces
class CreateWorkspaceRequestBody(RequestBody, WorkspaceCreate):
    """Request body for the create workspace endpoint."""


class CreateWorkspaceResponseBody(ResponseBody, WorkspacesResponse):
    """Response body for the create workspace endpoint."""


# PUT /workspaces/{workspace_id}
class UpdateWorkspacePathParameters(PathParameters):
    """Path parameters for the update workspace endpoint."""

    workspace_id: str


class UpdateWorkspaceRequestBody(RequestBody, WorkspaceUpdate):
    """Request body for the update workspace endpoint."""


class UpdateWorkspaceResponseBody(ResponseBody, WorkspacesResponse):
    """Response body for the update workspace endpoint."""


# DELETE /workspaces/{workspace_id}
class DeleteWorkspacePathParameters(PathParameters):
    """Path parameters for the delete workspace endpoint."""

    workspace_id: str


class DeleteWorkspaceResponseBody(ResponseBody, WorkspacesResponse):
    """Response body for the delete workspace endpoint."""
