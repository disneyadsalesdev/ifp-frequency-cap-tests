"""Search INFORMATION_SCHEMA for sales child line item id columns."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

SERVER = Path(r"C:\Users\syeda012\projects\rym-work\snowflake-mcp-server\server.py")

for key, value in {
    "SNOWFLAKE_ACCOUNT": "DISNEYSTREAMING-HULUX",
    "SNOWFLAKE_HOST": "DISNEYSTREAMING-HULUX.snowflakecomputing.com",
    "SNOWFLAKE_USER": "AHMED.SYED@DISNEY.COM",
    "SNOWFLAKE_AUTHENTICATOR": "externalbrowser",
    "SNOWFLAKE_ROLE": "ATO_BASIC",
    "SNOWFLAKE_WAREHOUSE": "ATO_REGULAR",
    "SNOWFLAKE_DATABASE": "UNIVERSE360",
    "SNOWFLAKE_SCHEMA": "ADVERTISING",
}.items():
    os.environ.setdefault(key, value)

spec = importlib.util.spec_from_file_location("sf", SERVER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

queries = {
    "child + li + id patterns": """
        SELECT table_name, column_name, data_type
        FROM UNIVERSE360.INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'ADVERTISING'
          AND (
            UPPER(column_name) LIKE '%SALES%CHILD%LI%'
            OR UPPER(column_name) LIKE '%CHILD%LI%ID%'
            OR UPPER(column_name) LIKE '%SALES%CHILD%'
            OR UPPER(column_name) = 'SALES_CHILD_LI_ID'
            OR UPPER(column_name) LIKE '%SALESCHILD%'
          )
        ORDER BY column_name, table_name
        LIMIT 200
    """,
    "line item id variants": """
        SELECT table_name, column_name, data_type
        FROM UNIVERSE360.INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'ADVERTISING'
          AND (
            UPPER(column_name) LIKE '%LINE%ITEM%ID%'
            OR UPPER(column_name) = 'LINE_ITEM_ID'
            OR UPPER(column_name) LIKE '%LI_ID%'
          )
        ORDER BY column_name, table_name
        LIMIT 100
    """,
}

for title, sql in queries.items():
    print(f"\n=== {title} ===")
    payload = json.loads(mod.run_sql(sql, max_rows=200))
    rows = payload.get("rows", [])
    print(f"matches: {len(rows)}")
    seen: set[tuple[str, str]] = set()
    for row in rows:
        table = row.get("TABLE_NAME") or row.get("table_name")
        column = row.get("COLUMN_NAME") or row.get("column_name")
        dtype = row.get("DATA_TYPE") or row.get("data_type")
        key = (column, table)
        if key in seen:
            continue
        seen.add(key)
        print(f"  {table}.{column} ({dtype})")
