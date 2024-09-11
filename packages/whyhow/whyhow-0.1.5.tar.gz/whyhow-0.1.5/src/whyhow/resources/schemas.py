"""Schemas resource."""

import json
import logging
from pathlib import Path
from typing import AsyncIterator, Iterator

from whyhow.raw import (
    CreateSchemaRequestBody,
    SchemaEntityFieldRaw,
    SchemaEntityRaw,
    SchemaRaw,
    SchemaRelationRaw,
    SchemaSlimRaw,
    SchemaTriplePatternRaw,
    SchemaTriplePatternSlimRaw,
    acreate_schema,
    adelete_schema,
    agenerate_schema,
    aget_all_schemas,
    aget_schema,
    create_schema,
    delete_schema,
    generate_schema,
    get_all_schemas,
    get_schema,
)
from whyhow.resources.base import AsyncResource, Resource, validate
from whyhow.schemas import (
    Schema,
    SchemaEntity,
    SchemaEntityField,
    SchemaRelation,
    SchemaTriplePattern,
)

logger = logging.getLogger(__name__)


def load_json(
    file_path: str | Path,
) -> tuple[
    list[SchemaEntity], list[SchemaRelation], list[SchemaTriplePattern]
]:
    """Load a JSON file containing a schema."""
    path = Path(file_path)

    with path.open("r") as f:
        data = json.load(f)

    entity_types_key = "entity_types"
    if entity_types_key not in data:
        logger.warning(f"`{entity_types_key}` not found in the schema file.")
        entity_types_key = "entities"
        logger.warning(f"Using `{entity_types_key}` instead.")
    entities = [SchemaEntity(**e) for e in data[entity_types_key]]
    relations = [SchemaRelation(**r) for r in data["relations"]]

    name2entity = {e.name: e for e in entities}
    name2relation = {r.name: r for r in relations}

    if len(name2entity) != len(entities):
        raise ValueError("Duplicate entity names")

    if len(name2relation) != len(relations):
        raise ValueError("Duplicate relation names")

    patterns = []

    for p in data["patterns"]:
        head = name2entity[p["head"]]
        relation = name2relation[p["relation"]]
        tail = name2entity[p["tail"]]
        pattern = SchemaTriplePattern(
            head=head,
            relation=relation,
            tail=tail,
            description=p["description"],
        )
        patterns.append(pattern)

    return entities, relations, patterns


def rawerp2publicerp(
    entities: list[SchemaEntityRaw],
    relations: list[SchemaRelationRaw],
    patterns: list[SchemaTriplePatternSlimRaw] | list[SchemaTriplePatternRaw],
) -> tuple[
    list[SchemaEntity],
    list[SchemaRelation],
    list[SchemaTriplePattern],
]:
    """Convert raw entities, relations and patterns to public entities, relations and patterns."""
    entities_pub = [
        SchemaEntity(
            name=e.name,
            description=e.description,
            fields=[
                SchemaEntityField(**f.model_dump()) for f in (e.fields or [])
            ],
        )
        for e in entities
    ]

    relations_pub = [
        SchemaRelation(
            name=r.name,
            description=r.description,
        )
        for r in relations
    ]

    name2entity = {e.name: e for e in entities_pub}
    name2relation = {r.name: r for r in relations_pub}

    patterns_pub: list[SchemaTriplePattern] = []

    for pattern in patterns:
        if isinstance(pattern, SchemaTriplePatternRaw):
            patterns_pub.append(
                SchemaTriplePattern(
                    head=name2entity[pattern.head.name],
                    relation=name2relation[pattern.relation.name],
                    tail=name2entity[pattern.tail.name],
                    description=pattern.description,
                )
            )
        else:
            patterns_pub.append(
                SchemaTriplePattern(
                    head=name2entity[pattern.head],
                    relation=name2relation[pattern.relation],
                    tail=name2entity[pattern.tail],
                    description=pattern.description,
                )
            )

    return entities_pub, relations_pub, patterns_pub


def raw2public(schema: SchemaRaw | SchemaSlimRaw) -> Schema:
    """Convert a raw schema to a public schema."""
    entities, relations, patterns = rawerp2publicerp(
        schema.entities, schema.relations, schema.patterns
    )

    if isinstance(schema, SchemaRaw):
        workspace_id = schema.workspace.field_id
    else:
        workspace_id = schema.workspace_id

    retval = Schema(
        schema_id=schema.field_id,
        workspace_id=workspace_id,
        name=schema.name,
        entities=entities,
        relations=relations,
        patterns=patterns,
        created_at=schema.created_at,
        updated_at=schema.updated_at,
    )

    return retval


def public2raw(
    entities: list[SchemaEntity],
    relations: list[SchemaRelation],
    patterns: list[SchemaTriplePattern],
) -> tuple[
    list[SchemaEntityRaw],
    list[SchemaRelationRaw],
    list[SchemaTriplePatternSlimRaw],
]:
    """Convert public schema to raw schema."""
    entities_raw = [
        SchemaEntityRaw(
            name=e.name,
            description=e.description,
            fields=[SchemaEntityFieldRaw(**f.model_dump()) for f in e.fields],
        )
        for e in entities
    ]

    relations_raw = [
        SchemaRelationRaw(
            name=r.name,
            description=r.description,
        )
        for r in relations
    ]

    patterns_raw = [
        SchemaTriplePatternSlimRaw(
            head=p.head.name,
            relation=p.relation.name,
            tail=p.tail.name,
            description=p.description,
        )
        for p in patterns
    ]

    return entities_raw, relations_raw, patterns_raw


class SchemasResource(Resource):
    """Schemas resource."""

    @staticmethod
    def load_json(
        file_path: str | Path,
    ) -> tuple[
        list[SchemaEntity], list[SchemaRelation], list[SchemaTriplePattern]
    ]:
        """Load a JSON file containing a schema.

        Parameters
        ----------
        file_path
            The file path.

        Returns
        -------
        list[SchemaEntity]
            The schema entities.

        list[SchemaRelation]
            The schema relations.

        list[SchemaTriplePattern]
            The schema patterns.
        """
        return load_json(file_path)

    def get(self, schema_id: str) -> Schema:
        """
        Get a schema.

        Parameters
        ----------
        schema_id : str
            The schema ID.

        Returns
        -------
        Schema
            The schema.
        """
        result = get_schema(self.client, schema_id)
        body = validate(result)

        if body.schemas is None or len(body.schemas) == 0:
            raise ValueError("No schema found")

        schema_raw = body.schemas[0]

        retval = raw2public(schema_raw)
        return retval

    def get_all(
        self,
        limit: int = 10,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
    ) -> Iterator[Schema]:
        """
        Get all schemas.

        Parameters
        ----------
        limit : int, optional
            The maximum number of schemas to fetch in one request.

        workspace_id : str, optional
            The workspace ID.

        workspace_name : str, optional
            The workspace name.

        Returns
        -------
        Iterator[Schema]
            The schema iterator.

        Yields
        ------
        Schema
            A schema.
        """
        skip = 0

        while True:
            result = get_all_schemas(
                self.client,
                limit=limit,
                skip=skip,
                workspace_id=workspace_id,
                workspace_name=workspace_name,
            )
            body = validate(result)

            if body.schemas is None:
                break

            for schema_raw in body.schemas:
                skip += 1
                retval = raw2public(schema_raw)
                yield retval

            if len(body.schemas) < limit:
                break

    def create(
        self,
        name: str,
        workspace_id: str,
        entities: list[SchemaEntity],
        relations: list[SchemaRelation],
        patterns: list[SchemaTriplePattern],
    ) -> Schema:
        """
        Create a schema.

        Parameters
        ----------
        name : str
            The schema name.

        workspace_id : str
            The workspace ID.

        entities : list[SchemaEntity]
            The schema entities.

        relations : list[SchemaRelation]
            The schema relations.

        patterns : list[TriplePattern]
            The schema patterns.

        Returns
        -------
        Schema
            The schema.
        """
        entities_raw, relations_raw, patterns_raw = public2raw(
            entities, relations, patterns
        )

        request_body = CreateSchemaRequestBody(
            name=name,
            workspace=workspace_id,
            entities=entities_raw,
            relations=relations_raw,
            patterns=patterns_raw,
        )
        result = create_schema(self.client, body=request_body)
        body = validate(result)

        schema_raw = body.schemas[0]

        retval = raw2public(schema_raw)
        return retval

    def delete(self, schema_id: str) -> Schema:
        """
        Delete a schema.

        Parameters
        ----------
        schema_id : str
            The schema ID.

        Returns
        -------
        Schema
            The schema.
        """
        result = delete_schema(self.client, schema_id)

        body = validate(result)

        schema_raw = body.schemas[0]

        retval = raw2public(schema_raw)

        return retval

    def generate(
        self, questions: list[str]
    ) -> tuple[
        list[SchemaEntity], list[SchemaRelation], list[SchemaTriplePattern]
    ]:
        """
        Generate a schema.

        Parameters
        ----------
        questions : list[str]
            The questions.

        Returns
        -------
        entities : list[SchemaEntity]
            The schema entities.

        relations : list[SchemaRelation]
            The schema relations.

        patterns : list[SchemaTriplePattern]
            The schema patterns.
        """
        result = generate_schema(self.client, questions=questions)
        body = validate(result)

        schema_raw = body.generated_schema

        entities, relations, patterns = rawerp2publicerp(
            schema_raw.entities, schema_raw.relations, schema_raw.patterns
        )

        return entities, relations, patterns


class AsyncSchemasResource(AsyncResource):
    """Async schemas resource."""

    @staticmethod
    def load_json(
        file_path: str | Path,
    ) -> tuple[
        list[SchemaEntity], list[SchemaRelation], list[SchemaTriplePattern]
    ]:
        """Load a JSON file containing a schema.

        Parameters
        ----------
        file_path
            The file path.

        Returns
        -------
        list[SchemaEntity]
            The schema entities.

        list[SchemaRelation]
            The schema relations.

        list[SchemaTriplePattern]
            The schema patterns.
        """
        return load_json(file_path)

    async def get(self, schema_id: str) -> Schema:
        """
        Get a schema.

        Parameters
        ----------
        schema_id : str
            The schema ID.

        Returns
        -------
        Schema
            The schema.
        """
        result = await aget_schema(self.client, schema_id)
        body = validate(result)

        if body.schemas is None or len(body.schemas) == 0:
            raise ValueError("No schema found")

        schema_raw = body.schemas[0]

        retval = raw2public(schema_raw)
        return retval

    async def get_all(
        self,
        limit: int = 10,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
    ) -> AsyncIterator[Schema]:
        """
        Get all schemas.

        Parameters
        ----------
        limit : int, optional
            The maximum number of schemas to fetch in one request.

        workspace_id : str, optional
            The workspace ID.

        workspace_name : str, optional
            The workspace name.

        Returns
        -------
        AsyncIterator[Schema]
            The schema iterator.

        Yields
        ------
        Schema
            A schema.
        """
        skip = 0

        while True:
            result = await aget_all_schemas(
                self.client,
                limit=limit,
                skip=skip,
                workspace_id=workspace_id,
                workspace_name=workspace_name,
            )
            body = validate(result)

            if body.schemas is None:
                break

            for schema_raw in body.schemas:
                skip += 1
                retval = raw2public(schema_raw)
                yield retval

            if len(body.schemas) < limit:
                break

    async def create(
        self,
        name: str,
        workspace_id: str,
        entities: list[SchemaEntity],
        relations: list[SchemaRelation],
        patterns: list[SchemaTriplePattern],
    ) -> Schema:
        """
        Create a schema.

        Parameters
        ----------
        name : str
            The schema name.

        workspace_id : str
            The workspace ID.

        entities : list[SchemaEntity]
            The schema entities.

        relations : list[SchemaRelation]
            The schema relations.

        patterns : list[TriplePattern]
            The schema patterns.

        Returns
        -------
        Schema
            The schema.
        """
        entities_raw, relations_raw, patterns_raw = public2raw(
            entities, relations, patterns
        )

        request_body = CreateSchemaRequestBody(
            name=name,
            workspace=workspace_id,
            entities=entities_raw,
            relations=relations_raw,
            patterns=patterns_raw,
        )
        result = await acreate_schema(self.client, body=request_body)
        body = validate(result)

        schema_raw = body.schemas[0]

        retval = raw2public(schema_raw)
        return retval

    async def delete(self, schema_id: str) -> Schema:
        """
        Delete a schema.

        Parameters
        ----------
        schema_id : str
            The schema ID.

        Returns
        -------
        Schema
            The schema.
        """
        result = await adelete_schema(self.client, schema_id)

        body = validate(result)

        schema_raw = body.schemas[0]

        retval = raw2public(schema_raw)

        return retval

    async def generate(
        self, questions: list[str]
    ) -> tuple[
        list[SchemaEntity], list[SchemaRelation], list[SchemaTriplePattern]
    ]:
        """
        Generate a schema.

        Parameters
        ----------
        questions : list[str]
            The questions.

        Returns
        -------
        entities : list[SchemaEntity]
            The schema entities.

        relations : list[SchemaRelation]
            The schema relations.

        patterns : list[SchemaTriplePattern]
            The schema patterns.
        """
        result = await agenerate_schema(self.client, questions=questions)
        body = validate(result)

        schema_raw = body.generated_schema

        entities, relations, patterns = rawerp2publicerp(
            schema_raw.entities, schema_raw.relations, schema_raw.patterns
        )

        return entities, relations, patterns
