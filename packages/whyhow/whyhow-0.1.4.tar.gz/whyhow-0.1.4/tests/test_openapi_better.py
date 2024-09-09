import importlib.util
import inspect
import subprocess
from typing import Any

import pytest

import whyhow.raw as raw_module
from whyhow.raw.base import RequestBody, ResponseBody

SERVER_URL = "http://localhost:8001"


def check_equal(
    obj_1: str | int | float | None | bool | dict[str, Any] | list[Any],
    defs_1: dict[str, Any],
    obj_2: str | int | float | None | bool | dict[str, Any] | list[Any],
    defs_2: dict[str, Any],
) -> None:
    EXCLUDED_KEYS = {"title", "description", "example"}

    if type(obj_1) is not type(obj_2):
        assert False

    if isinstance(obj_1, (str, int, float, bool, type(None))):
        assert obj_1 == obj_2

    elif isinstance(obj_1, list):
        assert len(obj_1) == len(obj_2)

        for i, v in enumerate(obj_1):
            check_equal(
                obj_1=v,
                defs_1=defs_1,
                obj_2=obj_2[i],
                defs_2=defs_2,
            )

    elif isinstance(obj_1, dict):
        keys_1 = {k for k in obj_1.keys() if k not in EXCLUDED_KEYS}
        keys_2 = {k for k in obj_2.keys() if k not in EXCLUDED_KEYS}

        assert keys_1 == keys_2

        for k, v in obj_1.items():
            if k in EXCLUDED_KEYS:
                continue

            if k == "$ref":
                new_obj_1 = defs_1[v.split("/")[-1]]
                new_obj_2 = defs_2[obj_2[k].split("/")[-1]]

                check_equal(
                    obj_1=new_obj_1,
                    defs_1=defs_1,
                    obj_2=new_obj_2,
                    defs_2=defs_2,
                )

            else:
                check_equal(
                    obj_1=v,
                    defs_1=defs_1,
                    obj_2=obj_2[k],
                    defs_2=defs_2,
                )

    else:
        assert False, f"Unexpected type: {type(obj_1)}"


@pytest.fixture(scope="session")
def openapi_schemas(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "schemas.py"

    # Generate schema files
    subprocess.run(
        [
            "datamodel-codegen",
            "--enum-field-as-literal",
            "all",
            "--input-file-type",
            "openapi",
            "--use-annotated",
            "--reuse-model",
            "--output-model-type",
            "pydantic_v2.BaseModel",
            "--url",
            f"{SERVER_URL}/openapi.json",
            "--output",
            str(path),
        ],
        check=True,
    )

    # import dynamically generated module
    spec = importlib.util.spec_from_file_location("schemas", path)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    schemas = {
        name: cls for name, cls in inspect.getmembers(module, inspect.isclass)
    }

    return schemas


@pytest.mark.openapi
@pytest.mark.parametrize(
    "our_schema",
    [
        cls
        for _, cls in inspect.getmembers(raw_module, inspect.isclass)
        if issubclass(cls, (RequestBody, ResponseBody))
    ],
)
def test_(our_schema, openapi_schemas):
    # Our schemas inherit from auto-generated schemas

    autogen_parents = [p for p in our_schema.__mro__ if "autogen" in str(p)]

    # If a match is found, return the captured group (the response name)
    if not autogen_parents:
        assert (
            False
        ), f"{our_schema} does not inherit from any auto-generated schema"
    elif len(autogen_parents) == 1:
        openapi_schema_name = autogen_parents[0].__name__
    else:
        assert False, f"Multiple auto-generated schemas found in {our_schema}"

    if openapi_schema_name not in openapi_schemas:
        pytest.skip("Linked OpenAPI schema not found")

    openapi_schema = openapi_schemas[openapi_schema_name].model_json_schema()
    our_schema = our_schema.model_json_schema()

    our_properties = our_schema["properties"].keys()
    openapi_properties = openapi_schema["properties"].keys()
    assert set(our_properties) == set(openapi_properties)

    openapi_required = our_schema.get("required", [])
    our_required = our_schema.get("required", [])
    assert set(openapi_required) == set(our_required)

    check_equal(
        obj_1={
            "properties": our_schema["properties"],
            "required": our_schema.get("required", []),
        },
        defs_1=our_schema.get("$defs", {}),
        obj_2={
            "properties": openapi_schema["properties"],
            "required": openapi_schema.get("required", []),
        },
        defs_2=openapi_schema.get("$defs", {}),
    )
