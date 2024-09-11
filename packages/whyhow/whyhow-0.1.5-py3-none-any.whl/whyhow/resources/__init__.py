"""Collection of route specific resources."""

from whyhow.resources.chunks import AsyncChunksResource, ChunksResource
from whyhow.resources.documents import (
    AsyncDocumentsResource,
    DocumentsResource,
)
from whyhow.resources.graphs import AsyncGraphsResource, GraphsResource
from whyhow.resources.schemas import AsyncSchemasResource, SchemasResource
from whyhow.resources.workspaces import (
    AsyncWorkspacesResource,
    WorkspacesResource,
)

__all__ = [
    "AsyncChunksResource",
    "AsyncDocumentsResource",
    "AsyncGraphsResource",
    "AsyncSchemasResource",
    "AsyncWorkspacesResource",
    "ChunksResource",
    "DocumentsResource",
    "GraphsResource",
    "SchemasResource",
    "WorkspacesResource",
]
