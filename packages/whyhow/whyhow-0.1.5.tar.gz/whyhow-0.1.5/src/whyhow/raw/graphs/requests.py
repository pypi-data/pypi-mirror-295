"""Requests."""

from typing import Literal

from httpx import AsyncClient, Client

from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.graphs.schemas import (
    AddChunksToGraphRequestBody,
    AddChunksToGraphResponseBody,
    AddTriplesToGraphRequestBody,
    AddTriplesToGraphResponseBody,
    CreateGraphFromTriplesRequestBody,
    CreateGraphFromTriplesResponseBody,
    CreateGraphRequestBody,
    CreateGraphResponseBody,
    ExportGraphCypherPathParameters,
    ExportGraphCypherResponseBody,
    GetAllGraphsQueryParameters,
    GetAllGraphsResponseBody,
    GetGraphPathParameters,
    GetGraphResponseBody,
    GetGraphTriplesPathParameters,
    GetGraphTriplesQueryParameters,
    GetGraphTriplesResponseBody,
    GraphNameRaw,
    GraphQueryRaw,
    QueryGraphPathParameters,
    QueryGraphRequestBody,
    QueryGraphResponseBody,
    UpdateGraphPathParameters,
    UpdateGraphRequestBody,
    UpdateGraphResponseBody,
)


# sync functions
def get_graph(
    client: Client, graph_id: str
) -> SuccessReturnType[GetGraphResponseBody] | ErrorReturnType:
    """Get a graph by its ID."""
    url = "/graphs/{graph_id}"
    path_parameters = GetGraphPathParameters(graph_id=graph_id)

    return send(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=GetGraphResponseBody,
    )


def get_all_graphs(
    client: Client,
    skip: int | None = None,
    limit: int | None = None,
    name: str | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    schema_id: str | None = None,
    schema_name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllGraphsResponseBody] | ErrorReturnType:
    """Get all graphs."""
    url = "/graphs"
    query_parameters = GetAllGraphsQueryParameters(
        skip=skip,
        limit=limit,
        name=name,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        schema_id=schema_id,
        schema_name=schema_name,
        order=order,
    )

    return send(
        client=client,
        method="get",
        url=url,
        query_parameters=query_parameters,
        response_body_schema=GetAllGraphsResponseBody,
    )


def create_graph(
    client: Client, body: CreateGraphRequestBody
) -> SuccessReturnType[CreateGraphResponseBody] | ErrorReturnType:
    """Create a graph."""
    url = "/graphs"

    return send(
        client=client,
        method="post",
        url=url,
        request_body=body,
        response_body_schema=CreateGraphResponseBody,
    )


def update_graph(
    client: Client,
    graph_id: str,
    name: str | None = None,
    public: bool | None = None,
) -> SuccessReturnType[UpdateGraphResponseBody] | ErrorReturnType:
    """Update a graph by its ID."""
    url = "/graphs/{graph_id}"
    path_parameters = UpdateGraphPathParameters(graph_id=graph_id)
    request_body = UpdateGraphRequestBody(
        name=GraphNameRaw(root=name) if name is not None else None,
        public=public,
    )

    return send(
        client=client,
        method="put",
        url=url,
        path_parameters=path_parameters,
        request_body=request_body,
        response_body_schema=UpdateGraphResponseBody,
    )


def export_graph_cypher(
    client: Client, graph_id: str
) -> SuccessReturnType[ExportGraphCypherResponseBody] | ErrorReturnType:
    """Export a graph as a Cypher query."""
    url = "/graphs/{graph_id}/export/cypher"
    path_parameters = ExportGraphCypherPathParameters(graph_id=graph_id)

    return send(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=ExportGraphCypherResponseBody,
    )


def query_graph_unstructured(
    client: Client,
    graph_id: str,
    query: str,
    return_answer: bool,
    include_chunks: bool,
) -> SuccessReturnType[QueryGraphResponseBody] | ErrorReturnType:
    """Query a graph."""
    url = "/graphs/{graph_id}/query"
    path_parameters = QueryGraphPathParameters(graph_id=graph_id)

    body = QueryGraphRequestBody(
        query=GraphQueryRaw(root=query),
        return_answer=return_answer,
        include_chunks=include_chunks,
        entities=None,
        relations=None,
        values=None,
    )

    return send(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=QueryGraphResponseBody,
    )


def query_graph_structured(
    client: Client,
    graph_id: str,
    entities: list[str] | None = None,
    relations: list[str] | None = None,
    values: list[str] | None = None,
) -> SuccessReturnType[QueryGraphResponseBody] | ErrorReturnType:
    """Query a graph."""
    url = "/graphs/{graph_id}/query"
    path_parameters = QueryGraphPathParameters(graph_id=graph_id)

    body = QueryGraphRequestBody(
        query=None,
        return_answer=False,
        include_chunks=False,
        entities=entities,
        relations=relations,
        values=values,
    )

    return send(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=QueryGraphResponseBody,
    )


def get_all_triples(
    client: Client,
    graph_id: str,
    skip: int | None = None,
    limit: int | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetGraphTriplesResponseBody] | ErrorReturnType:
    """Get all triples of a graph."""
    url = "/graphs/{graph_id}/triples"
    path_parameters = GetGraphTriplesPathParameters(graph_id=graph_id)
    query_parameters = GetGraphTriplesQueryParameters(
        skip=skip, limit=limit, order=order
    )

    return send(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        query_parameters=query_parameters,
        response_body_schema=GetGraphTriplesResponseBody,
    )


def create_graph_from_triples(
    client: Client, body: CreateGraphFromTriplesRequestBody
) -> SuccessReturnType[CreateGraphFromTriplesResponseBody] | ErrorReturnType:
    """Create a graph from triples."""
    url = "/graphs/from_triples"

    return send(
        client=client,
        method="post",
        url=url,
        request_body=body,
        response_body_schema=CreateGraphFromTriplesResponseBody,
    )


def add_chunks_to_graph(
    client: Client,
    body: AddChunksToGraphRequestBody,
) -> SuccessReturnType[AddChunksToGraphResponseBody] | ErrorReturnType:
    """Add chunks to a graph."""
    url = "/graphs/add_chunks"

    return send(
        client=client,
        method="put",
        url=url,
        request_body=body,
        response_body_schema=AddChunksToGraphResponseBody,
    )


def add_triples_to_graph(
    client: Client,
    body: AddTriplesToGraphRequestBody,
) -> SuccessReturnType[AddTriplesToGraphResponseBody] | ErrorReturnType:
    """Add triples to a graph."""
    url = "/triples"

    return send(
        client=client,
        method="post",
        url=url,
        request_body=body,
        response_body_schema=AddTriplesToGraphResponseBody,
    )


# async functions
async def aget_graph(
    client: AsyncClient, graph_id: str
) -> SuccessReturnType[GetGraphResponseBody] | ErrorReturnType:
    """Get a graph by its ID."""
    url = "/graphs/{graph_id}"
    path_parameters = GetGraphPathParameters(graph_id=graph_id)

    return await asend(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=GetGraphResponseBody,
    )


async def aget_all_graphs(
    client: AsyncClient,
    skip: int | None = None,
    limit: int | None = None,
    name: str | None = None,
    workspace_id: str | None = None,
    workspace_name: str | None = None,
    schema_id: str | None = None,
    schema_name: str | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllGraphsResponseBody] | ErrorReturnType:
    """Get all graphs."""
    url = "/graphs"
    query_parameters = GetAllGraphsQueryParameters(
        skip=skip,
        limit=limit,
        name=name,
        workspace_id=workspace_id,
        workspace_name=workspace_name,
        schema_id=schema_id,
        schema_name=schema_name,
        order=order,
    )

    return await asend(
        client=client,
        method="get",
        url=url,
        query_parameters=query_parameters,
        response_body_schema=GetAllGraphsResponseBody,
    )


async def acreate_graph(
    client: AsyncClient, body: CreateGraphRequestBody
) -> SuccessReturnType[CreateGraphResponseBody] | ErrorReturnType:
    """Create a graph."""
    url = "/graphs"

    return await asend(
        client=client,
        method="post",
        url=url,
        request_body=body,
        response_body_schema=CreateGraphResponseBody,
    )


async def aupdate_graph(
    client: AsyncClient,
    graph_id: str,
    name: str | None = None,
    public: bool | None = None,
) -> SuccessReturnType[UpdateGraphResponseBody] | ErrorReturnType:
    """Update a graph by its ID."""
    url = "/graphs/{graph_id}"
    path_parameters = UpdateGraphPathParameters(graph_id=graph_id)
    request_body = UpdateGraphRequestBody(
        name=GraphNameRaw(root=name) if name is not None else None,
        public=public,
    )

    return await asend(
        client=client,
        method="put",
        url=url,
        path_parameters=path_parameters,
        request_body=request_body,
        response_body_schema=UpdateGraphResponseBody,
    )


async def aexport_graph_cypher(
    client: AsyncClient, graph_id: str
) -> SuccessReturnType[ExportGraphCypherResponseBody] | ErrorReturnType:
    """Export a graph as a Cypher query."""
    url = "/graphs/{graph_id}/export/cypher"
    path_parameters = ExportGraphCypherPathParameters(graph_id=graph_id)

    return await asend(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        response_body_schema=ExportGraphCypherResponseBody,
    )


async def aquery_graph_unstructured(
    client: AsyncClient,
    graph_id: str,
    query: str,
    return_answer: bool,
    include_chunks: bool,
) -> SuccessReturnType[QueryGraphResponseBody] | ErrorReturnType:
    """Query a graph."""
    url = "/graphs/{graph_id}/query"
    path_parameters = QueryGraphPathParameters(graph_id=graph_id)

    body = QueryGraphRequestBody(
        query=GraphQueryRaw(root=query),
        return_answer=return_answer,
        include_chunks=include_chunks,
        entities=None,
        relations=None,
        values=None,
    )

    return await asend(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=QueryGraphResponseBody,
    )


async def aget_all_triples(
    client: AsyncClient,
    graph_id: str,
    skip: int | None = None,
    limit: int | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetGraphTriplesResponseBody] | ErrorReturnType:
    """Get all triples of a graph."""
    url = "/graphs/{graph_id}/triples"
    path_parameters = GetGraphTriplesPathParameters(graph_id=graph_id)
    query_parameters = GetGraphTriplesQueryParameters(
        skip=skip, limit=limit, order=order
    )

    return await asend(
        client=client,
        method="get",
        url=url,
        path_parameters=path_parameters,
        query_parameters=query_parameters,
        response_body_schema=GetGraphTriplesResponseBody,
    )


async def aquery_graph_structured(
    client: AsyncClient,
    graph_id: str,
    entities: list[str] | None = None,
    relations: list[str] | None = None,
    values: list[str] | None = None,
) -> SuccessReturnType[QueryGraphResponseBody] | ErrorReturnType:
    """Query a graph."""
    url = "/graphs/{graph_id}/query"
    path_parameters = QueryGraphPathParameters(graph_id=graph_id)

    body = QueryGraphRequestBody(
        query=None,
        return_answer=False,
        include_chunks=False,
        entities=entities,
        relations=relations,
        values=values,
    )

    return await asend(
        client=client,
        method="post",
        url=url,
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=QueryGraphResponseBody,
    )


async def acreate_graph_from_triples(
    client: AsyncClient, body: CreateGraphFromTriplesRequestBody
) -> SuccessReturnType[CreateGraphFromTriplesResponseBody] | ErrorReturnType:
    """Create a graph from triples."""
    url = "/graphs/from_triples"

    return await asend(
        client=client,
        method="post",
        url=url,
        request_body=body,
        response_body_schema=CreateGraphFromTriplesResponseBody,
    )


async def aadd_chunks_to_graph(
    client: AsyncClient, body: AddChunksToGraphRequestBody
) -> SuccessReturnType[AddChunksToGraphResponseBody] | ErrorReturnType:
    """Add chunks to a graph."""
    url = "/graphs/add_chunks"

    return await asend(
        client=client,
        method="put",
        url=url,
        request_body=body,
        response_body_schema=AddChunksToGraphResponseBody,
    )


async def aadd_triples_to_graph(
    client: AsyncClient, body: AddTriplesToGraphRequestBody
) -> SuccessReturnType[AddTriplesToGraphResponseBody] | ErrorReturnType:
    """Add triples to a graph."""
    url = "/triples"

    return await asend(
        client=client,
        method="post",
        url=url,
        request_body=body,
        response_body_schema=AddTriplesToGraphResponseBody,
    )
