from sqlalchemy.dialects.mysql import Insert, insert

from .types import RDBModel


def simple_upsert_stmt(
    values: list[RDBModel],
    ignore_keys: list[str] = None,
) -> Insert:
    if len(values) == 0:
        raise ValueError("No values provided")

    if ignore_keys is None:
        ignore_keys = ["id"]

    fields = [k for k in values[0].extract_fields().keys() if k not in ignore_keys]
    stmt = insert(values[0].__class__).values([u.extract_fields() for u in values])

    return stmt.on_duplicate_key_update(**{f: stmt.inserted[f] for f in fields})
