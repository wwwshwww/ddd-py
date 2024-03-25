import os


def get() -> list[str]:
    schema_path = os.getenv("DB_SCHEMA_PATH")
    schemas: list[str] = []
    with open(schema_path, encoding="utf-8", mode="r") as f:
        schemas = f.read().split(";")
    return schemas[:-1]  # 末尾に改行コードとかが入るのでトリムする


table_schemas: list[str] = get()
