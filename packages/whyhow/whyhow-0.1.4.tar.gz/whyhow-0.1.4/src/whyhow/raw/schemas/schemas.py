"""Collection of Pydantic models for the schemas router."""

from typing import Literal

from whyhow.raw.autogen import (
    EntityField,
    ErrorDetails,
    GeneratedSchema,
    GeneratedSchemaResponse,
    GenerateSchemaBody,
    SchemaCreate,
    SchemaEntity,
    SchemaOut,
    SchemaOutWithWorkspaceDetails,
    SchemaRelation,
    SchemasResponse,
    SchemasResponseWithWorkspaceDetails,
    SchemaTriplePattern,
    TriplePattern,
    WorkspaceDetails,
)
from whyhow.raw.base import (
    PathParameters,
    QueryParameters,
    RequestBody,
    ResponseBody,
)

# Auxiliary models
SchemaWorkspaceRaw = WorkspaceDetails
SchemaEntityFieldRaw = EntityField
SchemaEntityRaw = SchemaEntity
SchemaRelationRaw = SchemaRelation
SchemaTriplePatternRaw = SchemaTriplePattern
SchemaTriplePatternSlimRaw = TriplePattern
SchemaRaw = SchemaOutWithWorkspaceDetails
SchemaSlimRaw = SchemaOut
SchemaGeneratedRaw = GeneratedSchema
SchemaGenerationError = ErrorDetails


# GET /schemas/{schema_id}
class GetSchemaResponseBody(ResponseBody, SchemasResponseWithWorkspaceDetails):
    """Response model for the GET /schemas/{schema_id} endpoint."""


class GetSchemaPathParameters(PathParameters):
    """Path parameters for the GET /schemas/{schema_id} endpoint."""

    schema_id: str


# GET /schemas
class GetAllSchemasResponseBody(
    GetSchemaResponseBody, SchemasResponseWithWorkspaceDetails
):
    """Response model for the GET /schemas endpoint."""


class GetAllSchemasQueryParameters(QueryParameters):
    """Query parameters for the GET /schemas endpoint."""

    skip: int | None = None
    limit: int | None = None
    name: str | None = None
    workspace_id: str | None = None
    workspace_name: str | None = None
    order: Literal["ascending", "descending"] | None = None


# POST /schemas
class CreateSchemaRequestBody(RequestBody, SchemaCreate):
    """Request model for the POST /schemas endpoint."""


class CreateSchemaResponseBody(ResponseBody, SchemasResponse):
    """Response model for the POST /schemas endpoint."""


# DELETE /schemas/{schema_id}
class DeleteSchemaPathParameters(PathParameters):
    """Path parameters for the DELETE /schemas/{schema_id} endpoint."""

    schema_id: str


class DeleteSchemaResponseBody(ResponseBody, SchemasResponse):
    """Response model for the DELETE /schemas/{schema_id} endpoint."""


# POST /schemas/generate
class GenerateSchemaRequestBody(RequestBody, GenerateSchemaBody):
    """Request model for the POST /schemas/generate endpoint."""


class GenerateSchemaResponseBody(ResponseBody, GeneratedSchemaResponse):
    """Response model for the POST /schemas/generate endpoint."""
