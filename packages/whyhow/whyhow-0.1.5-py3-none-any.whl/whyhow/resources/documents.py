"""Documents resource."""

import logging
from asyncio import sleep as async_sleep
from pathlib import Path
from time import sleep
from typing import AsyncIterator, Iterator

from whyhow.exceptions import NotFoundError
from whyhow.raw import (
    adelete_document,
    agenerate_presigned_document,
    aget_all_documents,
    aget_document,
    aprocess_document,
    delete_document,
    generate_presigned_document,
    get_all_documents,
    get_document,
    process_document,
)
from whyhow.resources.base import AsyncResource, Resource, validate
from whyhow.schemas import Document, DocumentMetadata

logger = logging.getLogger(__name__)


class DocumentsResource(Resource):
    """Documents resource."""

    def _poll_document_in_db(
        self,
        document_id: str,
        max_seconds: int = 60,
        sleep_seconds: float = 1.5,
    ) -> Document:
        """Poll the document in the database."""
        elapsed_seconds = 0.0
        while True:
            try:
                doc = self.get(document_id=document_id)
            except NotFoundError:
                sleep(sleep_seconds)
                elapsed_seconds += sleep_seconds
                if elapsed_seconds > max_seconds:
                    raise ValueError("Something went wrong during upload")
                continue

            if doc.status == "uploaded":
                break

        return doc

    def _poll_document_processed(
        self,
        document_id: str,
        max_seconds: int = 60,
        sleep_seconds: float = 1.5,
    ) -> Document:
        """Poll the document processed."""
        elapsed_seconds = 0.0
        while True:
            doc = self.get(document_id=document_id)

            if doc.status in {"failed", "processed"}:
                break

            if doc.status == "processing":
                sleep(sleep_seconds)
                elapsed_seconds += sleep_seconds
                if elapsed_seconds > max_seconds:
                    raise ValueError(
                        "The processing is taking long. Please wait"
                    )

        return doc

    def get(self, document_id: str) -> Document:
        """
        Get documents.

        Parameters
        ----------
        document_id : str
            The document ID.

        Returns
        -------
        Document
            The document.
        """
        result = get_document(self.client, document_id=document_id)
        body = validate(result)

        if body.documents is None or len(body.documents) == 0:
            raise ValueError("Document not found")

        raw_doc = body.documents[0]

        doc = Document(
            document_id=raw_doc.field_id,
            created_at=raw_doc.created_at,
            updated_at=raw_doc.updated_at,
            workspace_ids=[w.field_id for w in raw_doc.workspaces],
            metadata=DocumentMetadata(
                size=raw_doc.metadata.size,
                format=raw_doc.metadata.format,
                filename=raw_doc.metadata.filename,
            ),
            status=raw_doc.status,
            tags=raw_doc.tags,
            user_metadata=raw_doc.user_metadata,
        )

        return doc

    def get_all(
        self,
        limit: int = 10,
        filename: str | None = None,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
    ) -> Iterator[Document]:
        """
        Get all documents.

        Parameters
        ----------
        limit : int, optional
            The number of documents to return.
        filename : str, optional
            The filename.
        workspace_id : str, optional
            The workspace ID.
        workspace_name : str, optional
            The workspace name.

        Returns
        -------
        Iterator[Document]
            The document iterator.

        Yields
        ------
        Document
            The document.
        """
        skip = 0

        while True:
            result = get_all_documents(
                self.client,
                skip=skip,
                limit=limit,
                filename=filename,
                workspace_id=workspace_id,
                workspace_name=workspace_name,
            )
            body = validate(result)

            if body.documents is None:
                break

            for raw_doc in body.documents:
                skip += 1
                doc = Document(
                    document_id=raw_doc.field_id,
                    created_at=raw_doc.created_at,
                    updated_at=raw_doc.updated_at,
                    workspace_ids=[w.field_id for w in raw_doc.workspaces],
                    metadata=DocumentMetadata(
                        size=raw_doc.metadata.size,
                        format=raw_doc.metadata.format,
                        filename=raw_doc.metadata.filename,
                    ),
                    status=raw_doc.status,
                    tags=raw_doc.tags,
                    user_metadata=raw_doc.user_metadata,
                )

                yield doc

            if len(body.documents) < limit:
                break

    def upload(
        self,
        path: str | Path,
        workspace_id: str,
        max_seconds: int = 60,
        sleep_seconds: float = 1.5,
    ) -> Document:
        """
        Upload a document.

        Parameters
        ----------
        path : Path
            The path to the document.
        workspace_id : str
            The workspace ID.
        max_seconds : int, optional
            The maximum number of seconds to wait for the document to be
            uploaded/processed.
        sleep_seconds : float, optional
            The number of seconds to sleep between polling.

        Returns
        -------
        Document
            The document.

        Raises
        ------
        FileNotFoundError
            If the file is not found.
        ValueError
            If the file format is not supported or the upload fails.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix
        if suffix not in [".csv", ".json", ".pdf", ".txt"]:
            raise ValueError(f"Unsupported file format: {suffix}")

        logger.info("Generating presigned URL for document upload.")
        result = generate_presigned_document(
            self.client,
            filename=path.name,
            workspace_id=workspace_id,
        )
        body = validate(result)

        logger.info("Uploading document to object store")
        document_id = body.fields["x-amz-meta-document-id"]

        response = self.client.post(
            url=body.url,
            data=body.fields,
            files={"file": path.open("rb")},
        )

        if response.status_code != 204:
            raise ValueError("Upload failed")

        logger.info("Waiting for metadata to be be put in the database.")
        _ = self._poll_document_in_db(
            document_id=document_id,
            max_seconds=max_seconds,
            sleep_seconds=sleep_seconds,
        )

        _ = process_document(self.client, document_id=document_id)

        logger.info("Processing document.")
        doc = self._poll_document_processed(
            document_id=document_id,
            max_seconds=max_seconds,
            sleep_seconds=sleep_seconds,
        )

        return doc

    def delete(self, document_id: str) -> Document:
        """
        Delete a document.

        Parameters
        ----------
        document_id : str
            The document ID.

        Returns
        -------
        Document
            The document.

        Raises
        ------
        ValueError
            If the document is deleted but not returned.
        """
        result = delete_document(self.client, document_id=document_id)
        body = validate(result)

        if body.documents is None:
            raise ValueError("Document deleted but not returned")

        doc_raw = body.documents[0]

        doc = Document(
            document_id=doc_raw.field_id,
            created_at=doc_raw.created_at,
            updated_at=doc_raw.updated_at,
            workspace_ids=doc_raw.workspaces,
            metadata=DocumentMetadata(
                size=doc_raw.metadata.size,
                format=doc_raw.metadata.format,
                filename=doc_raw.metadata.filename,
            ),
            status=doc_raw.status,
            tags=doc_raw.tags,
            user_metadata=doc_raw.user_metadata,
        )

        return doc


class AsyncDocumentsResource(AsyncResource):
    """Async documents resource."""

    async def _poll_document_in_db(
        self,
        document_id: str,
        max_seconds: int = 60,
        sleep_seconds: float = 1.5,
    ) -> Document:
        """Poll the document in the database."""
        elapsed_seconds = 0.0
        while True:
            try:
                doc = await self.get(document_id=document_id)
            except NotFoundError:
                await async_sleep(sleep_seconds)
                elapsed_seconds += sleep_seconds
                if elapsed_seconds > max_seconds:
                    raise ValueError("Something went wrong during upload")
                continue

            if doc.status == "uploaded":
                break

        return doc

    async def _poll_document_processed(
        self,
        document_id: str,
        max_seconds: int = 60,
        sleep_seconds: float = 1.5,
    ) -> Document:
        """Poll the document processed."""
        elapsed_seconds = 0.0
        while True:
            doc = await self.get(document_id=document_id)

            if doc.status in {"failed", "processed"}:
                break

            if doc.status == "processing":
                await async_sleep(sleep_seconds)
                elapsed_seconds += sleep_seconds
                if elapsed_seconds > max_seconds:
                    raise ValueError(
                        "The processing is taking long. Please wait"
                    )

        return doc

    async def get(self, document_id: str) -> Document:
        """
        Get documents.

        Parameters
        ----------
        document_id : str
            The document ID.

        Returns
        -------
        Document
            The document.
        """
        result = await aget_document(self.client, document_id=document_id)
        body = validate(result)

        if body.documents is None or len(body.documents) == 0:
            raise ValueError("Document not found")

        raw_doc = body.documents[0]

        doc = Document(
            document_id=raw_doc.field_id,
            created_at=raw_doc.created_at,
            updated_at=raw_doc.updated_at,
            workspace_ids=[w.field_id for w in raw_doc.workspaces],
            metadata=DocumentMetadata(
                size=raw_doc.metadata.size,
                format=raw_doc.metadata.format,
                filename=raw_doc.metadata.filename,
            ),
            status=raw_doc.status,
            tags=raw_doc.tags,
            user_metadata=raw_doc.user_metadata,
        )

        return doc

    async def get_all(
        self,
        limit: int = 10,
        filename: str | None = None,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
    ) -> AsyncIterator[Document]:
        """
        Get all documents.

        Parameters
        ----------
        limit : int, optional
            The number of documents to return.
        filename : str, optional
            The filename.
        workspace_id : str, optional
            The workspace ID.
        workspace_name : str, optional
            The workspace name.

        Returns
        -------
        AsyncIterator[Document]
            The document iterator.

        Yields
        ------
        Document
            The document.
        """
        skip = 0

        while True:
            result = await aget_all_documents(
                self.client,
                skip=skip,
                limit=limit,
                filename=filename,
                workspace_id=workspace_id,
                workspace_name=workspace_name,
            )
            body = validate(result)

            if body.documents is None:
                break

            for raw_doc in body.documents:
                skip += 1
                doc = Document(
                    document_id=raw_doc.field_id,
                    created_at=raw_doc.created_at,
                    updated_at=raw_doc.updated_at,
                    workspace_ids=[w.field_id for w in raw_doc.workspaces],
                    metadata=DocumentMetadata(
                        size=raw_doc.metadata.size,
                        format=raw_doc.metadata.format,
                        filename=raw_doc.metadata.filename,
                    ),
                    status=raw_doc.status,
                    tags=raw_doc.tags,
                    user_metadata=raw_doc.user_metadata,
                )

                yield doc

            if len(body.documents) < limit:
                break

    async def upload(
        self,
        path: str | Path,
        workspace_id: str,
        max_seconds: int = 60,
        sleep_seconds: float = 1.5,
    ) -> Document:
        """
        Upload a document.

        Parameters
        ----------
        path : Path
            The path to the document.
        workspace_id : str
            The workspace ID.
        max_seconds : int, optional
            The maximum number of seconds to wait for the document to be
            uploaded/processed.
        sleep_seconds : float, optional
            The number of seconds to sleep between polling.

        Returns
        -------
        Document
            The document.

        Raises
        ------
        FileNotFoundError
            If the file is not found.
        ValueError
            If the file format is not supported or the upload failed.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix
        if suffix not in [".csv", ".json", ".pdf", ".txt"]:
            raise ValueError(f"Unsupported file format: {suffix}")

        logger.info("Generating presigned URL for document upload.")
        result = await agenerate_presigned_document(
            self.client,
            filename=path.name,
            workspace_id=workspace_id,
        )
        body = validate(result)

        logger.info("Uploading document to object store")
        document_id = body.fields["x-amz-meta-document-id"]

        response = await self.client.post(
            url=body.url,
            data=body.fields,
            files={"file": path.open("rb")},
        )

        if response.status_code != 204:
            raise ValueError("Upload failed")

        logger.info("Waiting for metadata to be be put in the database.")
        _ = await self._poll_document_in_db(
            document_id=document_id,
            max_seconds=max_seconds,
            sleep_seconds=sleep_seconds,
        )

        _ = await aprocess_document(self.client, document_id=document_id)

        logger.info("Processing document.")
        doc = await self._poll_document_processed(
            document_id=document_id,
            max_seconds=max_seconds,
            sleep_seconds=sleep_seconds,
        )

        return doc

    async def delete(self, document_id: str) -> Document:
        """
        Delete a document.

        Parameters
        ----------
        document_id : str
            The document ID.

        Returns
        -------
        Document
            The document.

        Raises
        ------
        ValueError
            If the document is deleted but not returned.
        """
        result = await adelete_document(self.client, document_id=document_id)
        body = validate(result)

        if body.documents is None:
            raise ValueError("Document deleted but not returned")
        doc_raw = body.documents[0]

        doc = Document(
            document_id=doc_raw.field_id,
            created_at=doc_raw.created_at,
            updated_at=doc_raw.updated_at,
            workspace_ids=doc_raw.workspaces,
            metadata=DocumentMetadata(
                size=doc_raw.metadata.size,
                format=doc_raw.metadata.format,
                filename=doc_raw.metadata.filename,
            ),
            status=doc_raw.status,
            tags=doc_raw.tags,
            user_metadata=doc_raw.user_metadata,
        )

        return doc
