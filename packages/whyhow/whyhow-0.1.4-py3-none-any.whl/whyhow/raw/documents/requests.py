"""Documents requests."""

from typing import Literal

from httpx import AsyncClient, Client

from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.documents.schemas import (
    DeleteDocumentPathParameters,
    DeleteDocumentResponseBody,
    GeneratePresignedDocumentRequestBody,
    GeneratePresignedDocumentResponseBody,
    GetAllDocumentsQueryParameters,
    GetAllDocumentsResponseBody,
    GetDocumentPathParameters,
    GetDocumentResponseBody,
    ProcessDocumentResponseBody,
)


# sync functions
def get_document(
    client: Client,
    document_id: str,
) -> SuccessReturnType[GetDocumentResponseBody] | ErrorReturnType:
    """Get document by ID."""
    url = f"/documents/{document_id}"
    path_parameters = GetDocumentPathParameters(
        document_id=document_id,
    )
    return send(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=GetDocumentResponseBody,
    )


def get_all_documents(
    client: Client,
    skip: int | None = None,
    limit: int | None = None,
    filename: str | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllDocumentsResponseBody] | ErrorReturnType:
    """Get all documents."""
    url = "/documents"
    query_parameters = GetAllDocumentsQueryParameters(
        skip=skip,
        limit=limit,
        filename=filename,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        order=order,
    )

    return send(
        client=client,
        method="get",
        url=url,
        query_parameters=query_parameters,
        response_body_schema=GetAllDocumentsResponseBody,
    )


def generate_presigned_document(
    client: Client,
    filename: str,
    workspace_id: str,
) -> (
    SuccessReturnType[GeneratePresignedDocumentResponseBody] | ErrorReturnType
):
    """Generate presigned document."""
    url = "/documents/generate_presigned"
    request_body = GeneratePresignedDocumentRequestBody(
        filename=filename,
        workspace_id=workspace_id,
    )

    return send(
        client=client,
        method="post",
        url=url,
        request_body=request_body,
        response_body_schema=GeneratePresignedDocumentResponseBody,
    )


def process_document(
    client: Client,
    document_id: str,
) -> SuccessReturnType[ProcessDocumentResponseBody] | ErrorReturnType:
    """Process document by ID."""
    url = f"/documents/{document_id}/process"
    path_parameters = GetDocumentPathParameters(
        document_id=document_id,
    )
    return send(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=ProcessDocumentResponseBody,
    )


def delete_document(
    client: Client,
    document_id: str,
) -> SuccessReturnType[DeleteDocumentResponseBody] | ErrorReturnType:
    """Delete document by ID."""
    url = f"/documents/{document_id}"
    path_parameters = DeleteDocumentPathParameters(
        document_id=document_id,
    )
    return send(
        client=client,
        method="delete",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=DeleteDocumentResponseBody,
    )


# async functions
async def aget_document(
    client: AsyncClient,
    document_id: str,
) -> SuccessReturnType[GetDocumentResponseBody] | ErrorReturnType:
    """Get document by ID."""
    url = f"/documents/{document_id}"
    path_parameters = GetDocumentPathParameters(
        document_id=document_id,
    )
    return await asend(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=GetDocumentResponseBody,
    )


async def aget_all_documents(
    client: AsyncClient,
    skip: int | None = None,
    limit: int | None = None,
    filename: str | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllDocumentsResponseBody] | ErrorReturnType:
    """Get all documents."""
    url = "/documents"
    query_parameters = GetAllDocumentsQueryParameters(
        skip=skip,
        limit=limit,
        filename=filename,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        order=order,
    )

    return await asend(
        client=client,
        method="get",
        url=url,
        query_parameters=query_parameters,
        response_body_schema=GetAllDocumentsResponseBody,
    )


async def agenerate_presigned_document(
    client: AsyncClient,
    filename: str,
    workspace_id: str,
) -> (
    SuccessReturnType[GeneratePresignedDocumentResponseBody] | ErrorReturnType
):
    """Generate presigned document."""
    url = "/documents/generate_presigned"
    request_body = GeneratePresignedDocumentRequestBody(
        filename=filename,
        workspace_id=workspace_id,
    )

    return await asend(
        client=client,
        method="post",
        url=url,
        request_body=request_body,
        response_body_schema=GeneratePresignedDocumentResponseBody,
    )


async def aprocess_document(
    client: AsyncClient,
    document_id: str,
) -> SuccessReturnType[ProcessDocumentResponseBody] | ErrorReturnType:
    """Process document by ID."""
    url = f"/documents/{document_id}/process"
    path_parameters = GetDocumentPathParameters(
        document_id=document_id,
    )
    return await asend(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=ProcessDocumentResponseBody,
    )


async def adelete_document(
    client: AsyncClient,
    document_id: str,
) -> SuccessReturnType[DeleteDocumentResponseBody] | ErrorReturnType:
    """Delete document by ID."""
    url = f"/documents/{document_id}"
    path_parameters = DeleteDocumentPathParameters(
        document_id=document_id,
    )
    return await asend(
        client=client,
        method="delete",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=DeleteDocumentResponseBody,
    )
