"""Chunks resource."""

from typing import AsyncIterator, Iterator

from whyhow.raw import aget_all_chunks, aget_chunk, get_all_chunks, get_chunk
from whyhow.raw.chunks.requests import (
    aadd_chunks_to_workspace,
    add_chunks_to_workspace,
)
from whyhow.raw.chunks.schemas import (
    AddChunkModelRaw,
    AddChunksToWorkspaceRequestBody,
    ObjContentRaw,
    StrContentRaw,
)
from whyhow.resources.base import AsyncResource, Resource, validate
from whyhow.resources.utils import flatten_tags
from whyhow.schemas import Chunk, ChunkMetadata


class ChunksResource(Resource):
    """Chunk resource."""

    def get(
        self, chunk_id: str, include_embeddings: bool | None = None
    ) -> Chunk:
        """
        Get chunk by ID.

        Parameters
        ----------
        chunk_id : str
            The ID of the chunk.
        include_embeddings : bool, optional
            Whether to include embeddings.

        Returns
        -------
        Chunk
            The chunk.
        """
        result = get_chunk(
            client=self.client,
            chunk_id=chunk_id,
            include_embeddings=include_embeddings,
        )

        body = validate(result)

        if body.chunks is None or len(body.chunks) == 0:
            raise ValueError("Chunk not found")

        raw_chunk = body.chunks[0]

        if raw_chunk.document is None:
            document_id = None
        else:
            document_id = raw_chunk.document.field_id

        chunk = Chunk(
            chunk_id=raw_chunk.field_id,
            created_at=raw_chunk.created_at,
            updated_at=raw_chunk.updated_at,
            document_id=document_id,
            workspace_ids=[w.field_id for w in raw_chunk.workspaces],
            metadata=ChunkMetadata(
                language=raw_chunk.metadata.language,
                length=raw_chunk.metadata.length,
                size=raw_chunk.metadata.size,
                data_source_type=raw_chunk.metadata.data_source_type,
                index=raw_chunk.metadata.index,
                page=raw_chunk.metadata.page,
                start=raw_chunk.metadata.start,
                end=raw_chunk.metadata.end,
            ),
            content=raw_chunk.content.root,
            embedding=raw_chunk.embedding,
            tags=raw_chunk.tags,
            user_metadata=raw_chunk.user_metadata,
        )

        return chunk

    def get_all(
        self,
        limit: int = 10,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
        document_id: str | None = None,
        document_filename: str | None = None,
        include_embeddings: bool | None = None,
    ) -> Iterator[Chunk]:
        """
        Get all chunks.

        Parameters
        ----------
        limit : int, optional
            The number of chunks to return.
        workspace_id : str, optional
            The ID of the workspace.
        workspace_name : str, optional
            The name of the workspace.
        document_id : str, optional
            The ID of the document.
        document_filename : str, optional
            The filename of the document.
        include_embeddings : bool, optional
            Whether to include embeddings.

        Returns
        -------
        Iterator[Chunk]
            The chunk iterator.

        Yields
        ------
        Chunk
            The chunk.
        """
        skip = 0

        while True:
            result = get_all_chunks(
                client=self.client,
                skip=skip,
                limit=limit,
                workspace_id=workspace_id,
                workspace_name=workspace_name,
                document_id=document_id,
                document_filename=document_filename,
                include_embeddings=include_embeddings,
            )

            body = validate(result)

            if body.chunks is None:
                break

            for raw_chunk in body.chunks:
                skip += 1

                if raw_chunk.document is None:
                    document_id_ = None
                else:
                    document_id_ = raw_chunk.document.field_id

                chunk = Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    document_id=document_id_,
                    workspace_ids=[w.field_id for w in raw_chunk.workspaces],
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )

                yield chunk

            if len(body.chunks) < limit:
                break

    def create(self, workspace_id: str, chunks: list[Chunk]) -> list[Chunk]:
        """Add chunks to a workspace.

        Parameters
        ----------
        workspace_id : str
            The ID of the workspace.
        chunks : list[Chunk]
            The chunks to add.

        Returns
        -------
        list[Chunk]
            The updated chunks.
        """
        request_body = AddChunksToWorkspaceRequestBody(
            chunks=[
                AddChunkModelRaw(
                    content=StrContentRaw(root=chunk.content) if type(chunk.content) is str else ObjContentRaw(root=chunk.content),  # type: ignore
                    user_metadata=chunk.user_metadata,
                    tags=chunk.tags if type(chunk.tags) is list[str] else flatten_tags(chunk.tags),  # type: ignore
                )
                for chunk in chunks
            ]
        )
        result = add_chunks_to_workspace(
            self.client, workspace_id, request_body
        )
        body = validate(result)

        updated_chunks = []
        for raw_chunk in body.chunks:
            updated_chunks.append(
                Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    workspace_ids=raw_chunk.workspaces,
                    document_id=raw_chunk.document,
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )
            )

        return updated_chunks


class AsyncChunksResource(AsyncResource):
    """Chunk resource."""

    async def get(
        self, chunk_id: str, include_embeddings: bool | None = None
    ) -> Chunk:
        """
        Get chunk by ID.

        Parameters
        ----------
        chunk_id : str
            The ID of the chunk.
        include_embeddings : bool, optional
            Whether to include embeddings.

        Returns
        -------
        Chunk
            The chunk.
        """
        result = await aget_chunk(
            client=self.client,
            chunk_id=chunk_id,
            include_embeddings=include_embeddings,
        )

        body = validate(result)

        if body.chunks is None or len(body.chunks) == 0:
            raise ValueError("Chunk not found")

        raw_chunk = body.chunks[0]

        if raw_chunk.document is None:
            document_id = None
        else:
            document_id = raw_chunk.document.field_id

        chunk = Chunk(
            chunk_id=raw_chunk.field_id,
            created_at=raw_chunk.created_at,
            updated_at=raw_chunk.updated_at,
            document_id=document_id,
            workspace_ids=[w.field_id for w in raw_chunk.workspaces],
            metadata=ChunkMetadata(
                language=raw_chunk.metadata.language,
                length=raw_chunk.metadata.length,
                size=raw_chunk.metadata.size,
                data_source_type=raw_chunk.metadata.data_source_type,
                index=raw_chunk.metadata.index,
                page=raw_chunk.metadata.page,
                start=raw_chunk.metadata.start,
                end=raw_chunk.metadata.end,
            ),
            content=raw_chunk.content.root,
            embedding=raw_chunk.embedding,
            tags=raw_chunk.tags,
            user_metadata=raw_chunk.user_metadata,
        )

        return chunk

    async def get_all(
        self,
        limit: int = 10,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
        document_id: str | None = None,
        document_filename: str | None = None,
        include_embeddings: bool | None = None,
    ) -> AsyncIterator[Chunk]:
        """
        Get all chunks.

        Parameters
        ----------
        limit : int, optional
            The number of chunks to return.
        workspace_id : str, optional
            The ID of the workspace.
        workspace_name : str, optional
            The name of the workspace.
        document_id : str, optional
            The ID of the document.
        document_filename : str, optional
            The filename of the document.
        include_embeddings : bool, optional
            Whether to include embeddings.

        Returns
        -------
        AsyncIterator[Chunk]
            The chunk iterator.

        Yields
        ------
        Chunk
            The chunk.
        """
        skip = 0

        while True:
            result = await aget_all_chunks(
                client=self.client,
                skip=skip,
                limit=limit,
                workspace_id=workspace_id,
                workspace_name=workspace_name,
                document_id=document_id,
                document_filename=document_filename,
                include_embeddings=include_embeddings,
            )

            body = validate(result)

            if body.chunks is None:
                break

            for raw_chunk in body.chunks:
                skip += 1
                if raw_chunk.document is None:
                    document_id_ = None
                else:
                    document_id_ = raw_chunk.document.field_id

                chunk = Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    document_id=document_id_,
                    workspace_ids=[w.field_id for w in raw_chunk.workspaces],
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )

                yield chunk

            if len(body.chunks) < limit:
                break

    async def create(
        self, workspace_id: str, chunks: list[Chunk]
    ) -> list[Chunk]:
        """Add chunks to a workspace.

        Parameters
        ----------
        workspace_id : str
            The ID of the workspace.
        chunks : list[Chunk]
            The chunks to add.

        Returns
        -------
        list[Chunk]
            The updated chunks.
        """
        request_body = AddChunksToWorkspaceRequestBody(
            chunks=[
                AddChunkModelRaw(
                    content=StrContentRaw(root=chunk.content) if type(chunk.content) is str else ObjContentRaw(root=chunk.content),  # type: ignore
                    user_metadata=chunk.user_metadata,
                    tags=chunk.tags if type(chunk.tags) is list[str] else flatten_tags(chunk.tags),  # type: ignore
                )
                for chunk in chunks
            ]
        )
        result = await aadd_chunks_to_workspace(
            self.client, workspace_id, request_body
        )
        body = validate(result)

        updated_chunks = []
        for raw_chunk in body.chunks:
            updated_chunks.append(
                Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    workspace_ids=raw_chunk.workspaces,
                    document_id=raw_chunk.document,
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )
            )

        return updated_chunks
