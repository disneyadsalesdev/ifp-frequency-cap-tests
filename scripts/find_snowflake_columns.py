"""Search INFORMATION_SCHEMA for completion-related columns."""
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

sql = """
SELECT table_name, column_name, data_type
FROM UNIVERSE360.INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'ADVERTISING'
  AND (
    UPPER(column_name) LIKE '%DC%COMPLET%'
    OR UPPER(column_name) LIKE '%COMPLETION%'
  )
ORDER BY column_name, table_name
"""

payload = json.loads(mod.run_sql(sql, max_rows=500))
rows = payload.get("rows", [])

dc_rows = []
by_column: dict[str, list[str]] = {}
for row in rows:
    table = row.get("TABLE_NAME") or row.get("table_name")
    column = row.get("COLUMN_NAME") or row.get("column_name")
    dtype = row.get("DATA_TYPE") or row.get("data_type")
    upper = (column or "").upper()
    if "DC" in upper and "COMPLET" in upper:
        dc_rows.append((table, column, dtype))
    if "COMPLET" in upper and column:
        by_column.setdefault(column, []).append(table)

print("Total column matches:", len(rows))
print("\n=== DC + completion in column name ===")
if dc_rows:
    for table, column, dtype in dc_rows:
        print(f"  {table}.{column} ({dtype})")
else:
    print("  (no column name containing both DC and COMPLET)")

print("\n=== Distinct COMPLETION* column names and sample tables ===")
sql_dc = """
SELECT column_name, COUNT(*) AS table_count
FROM UNIVERSE360.INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'ADVERTISING'
  AND (
    UPPER(column_name) LIKE '%DPLUS%COMP%'
    OR UPPER(column_name) LIKE '%DISNEY%COMP%'
    OR UPPER(column_name) LIKE 'DC_%COMP%'
  )
GROUP BY column_name
ORDER BY column_name
"""

payload2 = json.loads(mod.run_sql(sql_dc, max_rows=100))
print("\n=== DPLUS / DISNEY / DC_*COMP* column names ===")
for row in payload2.get("rows", []):
    print(row)
