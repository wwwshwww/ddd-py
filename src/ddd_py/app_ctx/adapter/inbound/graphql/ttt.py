import os

from ariadne import (
    ObjectType,
    QueryType,
    SchemaBindable,
    make_executable_schema,
)

schema_path = os.getenv("GRAPHQL_SCHEMA_PATH_1")
schema_text: str = ""
if schema_path:
    with open(schema_path, encoding="utf-8") as f:
        schema_text = f.read()


query = QueryType()


a: list[SchemaBindable] = [
    ObjectType("A"),
    ObjectType("B"),
]
make_executable_schema(schema_text, *a, convert_names_case=True)
