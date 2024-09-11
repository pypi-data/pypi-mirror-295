"""Collection of Pydantic models for the the graphs router."""

from typing import Literal

from whyhow.raw.autogen import (
    AddChunksToGraphBody,
    ChunkFilters,
    CreateGraphBody,
    CreateGraphFromTriplesBody,
    CypherResponse,
    DetailedGraphsResponse,
    GraphsDetailedTripleResponse,
    GraphsResponse,
    GraphUpdate,
    Name,
    Query,
    QueryGraphRequest,
    TaskResponse,
    Triple,
    TripleCreate,
    TripleCreateNode,
    TriplesCreate,
)
from whyhow.raw.base import (
    PathParameters,
    QueryParameters,
    RequestBody,
    ResponseBody,
)

# Auxiliar models
GraphNameRaw = Name
GraphQueryRaw = Query
GraphChunkFiltersRaw = ChunkFilters
TripleRaw = Triple
TripleCreateRaw = TripleCreate
TripleCreateNodeRaw = TripleCreateNode


# GET /graphs/{graph_id}
class GetGraphPathParameters(PathParameters):
    """Path parameters for the get graph endpoint."""

    graph_id: str


class GetGraphResponseBody(ResponseBody, DetailedGraphsResponse):
    """Graph workspace model."""


# GET /graphs
class GetAllGraphsQueryParameters(QueryParameters):
    """Query parameters for the get all graphs endpoint."""

    skip: int | None = None
    limit: int | None = None
    name: str | None = None
    workspace_id: str | None = None
    workspace_name: str | None = None
    schema_id: str | None = None
    schema_name: str | None = None
    order: Literal["ascending", "descending"] | None = None


class GetAllGraphsResponseBody(ResponseBody, DetailedGraphsResponse):
    """Graph workspace model."""


# POST /graphs
class CreateGraphRequestBody(RequestBody, CreateGraphBody):
    """Create graph request body."""


class CreateGraphResponseBody(ResponseBody, GraphsResponse):
    """Graph workspace model."""


# PUT /graphs/{graph_id}
class UpdateGraphPathParameters(PathParameters):
    """Path parameters for the update graph endpoint."""

    graph_id: str


class UpdateGraphRequestBody(RequestBody, GraphUpdate):
    """Update graph request body."""


class UpdateGraphResponseBody(ResponseBody, GraphsResponse):
    """Update graph response body."""


# GET /graphs/{graph_id}/export/cypher
class ExportGraphCypherPathParameters(PathParameters):
    """Path parameters for the export cypher endpoint."""

    graph_id: str


class ExportGraphCypherResponseBody(ResponseBody, CypherResponse):
    """Extract cypher response body."""


# POST /graphs/{graph_id}/query
class QueryGraphPathParameters(PathParameters):
    """Path parameters for the query graph endpoint."""

    graph_id: str


class QueryGraphRequestBody(RequestBody, QueryGraphRequest):
    """Query graph request body."""


class QueryGraphResponseBody(ResponseBody, DetailedGraphsResponse):
    """Query graph response body."""


# GET /graphs/{graph_id}/triples
class GetGraphTriplesPathParameters(PathParameters):
    """Path parameters for the get graph triples endpoint."""

    graph_id: str


class GetGraphTriplesQueryParameters(QueryParameters):
    """Query parameters for the get graph triples endpoint."""

    skip: int | None = None
    limit: int | None = None
    order: Literal["ascending", "descending"] | None = None


class GetGraphTriplesResponseBody(ResponseBody, GraphsDetailedTripleResponse):
    """Graph triples response body."""


# POST /graphs/from_triples
class CreateGraphFromTriplesRequestBody(
    RequestBody, CreateGraphFromTriplesBody
):
    """Create graph from triples request body."""


class CreateGraphFromTriplesResponseBody(ResponseBody, GraphsResponse):
    """Create graph from triples response body."""


class AddChunksToGraphRequestBody(RequestBody, AddChunksToGraphBody):
    """Add chunks to graph request body."""


class AddChunksToGraphResponseBody(ResponseBody, GraphsResponse):
    """Add chunks to graph response body."""


class AddTriplesToGraphRequestBody(RequestBody, TriplesCreate):
    """Add triples to graph request body."""


class AddTriplesToGraphResponseBody(ResponseBody, TaskResponse):
    """Add triples to graph response body."""
