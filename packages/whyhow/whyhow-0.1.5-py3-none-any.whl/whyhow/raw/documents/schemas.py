"""Collection of Pydantic models for the the documents router."""

from typing import Literal

from whyhow.raw.autogen import (
    DocumentMetadata,
    DocumentOut,
    DocumentOutWithWorkspaceDetails,
    DocumentsResponse,
    DocumentsResponseWithWorkspaceDetails,
    GeneratePresignedRequest,
    GeneratePresignedResponse,
    WorkspaceDetails,
)
from whyhow.raw.base import (
    PathParameters,
    QueryParameters,
    RequestBody,
    ResponseBody,
)

# Auxiliary models
DocumentWorkspaceRaw = WorkspaceDetails
DocumentMetadataRaw = DocumentMetadata
DocumentRaw = DocumentOutWithWorkspaceDetails
DocumentSlimRaw = DocumentOut


# GET /documents/{}
class GetDocumentPathParameters(PathParameters):
    """Path parameters for GET /documents/{document_id}."""

    document_id: str


class GetDocumentResponseBody(
    ResponseBody, DocumentsResponseWithWorkspaceDetails
):
    """Response body for GET /documents/{document_id}."""


# GET /documents
class GetAllDocumentsQueryParameters(QueryParameters):
    """Query parameters for GET /documents."""

    skip: int | None = None
    limit: int | None = None
    filename: str | None = None
    workspace_id: str | None = None
    workspace_name: str | None = None
    order: Literal["ascending", "descending"] | None = None


class GetAllDocumentsResponseBody(
    ResponseBody, DocumentsResponseWithWorkspaceDetails
):
    """Response body for GET /documents."""


# POST /documents/generate_presigned
class GeneratePresignedDocumentRequestBody(
    RequestBody, GeneratePresignedRequest
):
    """Request body for POST /documents/generate_presigned."""


class GeneratePresignedDocumentResponseBody(
    ResponseBody, GeneratePresignedResponse
):
    """Response body for POST /documents/generate_presigned."""


# POST /documents/{document_id}/upload
class ProcessDocumentPathParameters(PathParameters):
    """Path parameters for POST /documents/{document_id}/upload."""

    document_id: str


class ProcessDocumentResponseBody(
    ResponseBody, DocumentsResponseWithWorkspaceDetails
):
    """Response body for POST /documents/{document_id}/upload."""


# DELETE /documents/{document_id}
class DeleteDocumentPathParameters(PathParameters):
    """Path parameters for DELETE /documents/{document_id}."""

    document_id: str


class DeleteDocumentResponseBody(ResponseBody, DocumentsResponse):
    """Response body for DELETE /documents/{document_id}."""
