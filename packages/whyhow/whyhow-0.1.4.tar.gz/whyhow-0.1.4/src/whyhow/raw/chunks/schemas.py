"""Collection of Pydantic models for the the chunks router."""

from typing import Literal

from whyhow.raw.autogen import (
    AddChunkModel,
    AddChunksModel,
    AddChunksResponse,
    ChunkMetadata,
    ChunksOutWithWorkspaceDetails,
    ChunksResponseWithWorkspaceDetails,
    Content,
    Content1,
    DocumentDetail,
    WorkspaceDetails,
)
from whyhow.raw.base import (
    PathParameters,
    QueryParameters,
    RequestBody,
    ResponseBody,
)

# Auxiliary models
ChunkWorkspaceRaw = WorkspaceDetails
ChunkDocumentDetailRaw = DocumentDetail
ChunkMetadataRaw = ChunkMetadata
ChunkRaw = ChunksOutWithWorkspaceDetails
AddChunkModelRaw = AddChunkModel
StrContentRaw = Content
ObjContentRaw = Content1


# GET /chunks/{chunk_id}
class GetChunkPathParameters(PathParameters):
    """Path parameters for the get chunk endpoint."""

    chunk_id: str


class GetChunkQueryParameters(QueryParameters):
    """Query parameters for the get chunk endpoint."""

    include_embeddings: bool | None = None


class GetChunkResponseBody(ResponseBody, ChunksResponseWithWorkspaceDetails):
    """Response body for the get chunk endpoint."""


# GET /chunks
class GetAllChunksQueryParameters(QueryParameters):
    """Query parameters for the get all chunks endpoint."""

    skip: int | None = None
    limit: int | None = None
    data_type: str | None = None
    workspace_id: str | None = None
    workspace_name: str | None = None
    worskpace_id: str | None = None
    document_id: str | None = None
    document_filename: str | None = None
    include_embeddings: bool | None = None
    order: Literal["ascending", "descending"] | None = None


class GetAllChunksResponseBody(
    ResponseBody, ChunksResponseWithWorkspaceDetails
):
    """Response body for the get all chunks endpoint."""


# POST /chunks/{workspace_id}
class AddChunksToWorkspacePathParameters(PathParameters):
    """Path parameters for the add chunks to workspace endpoint."""

    workspace_id: str


class AddChunksToWorkspaceRequestBody(RequestBody, AddChunksModel):
    """Add chunks to workspace request body."""


class AddChunksToWorkspaceResponseBody(ResponseBody, AddChunksResponse):
    """Add chunks to workspace response body."""
