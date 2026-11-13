"""Build the database in memory and run every named query in sql/queries.sql.

Usage:
    python src/run_queries.py
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def build_db(path: str = ":memory:") -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.executescript((ROOT / "sql" / "schema.sql").read_text())
    con.executescript((ROOT / "sql" / "seed_synthetic.sql").read_text())
    return con


def load_queries() -> dict[str, str]:
    text = (ROOT / "sql" / "queries.sql").read_text()
    parts = re.split(r"^-- name: (\w+)\s*$", text, flags=re.M)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


def run_all(con: sqlite3.Connection) -> dict[str, pd.DataFrame]:
    return {name: pd.read_sql_query(sql, con) for name, sql in load_queries().items()}


def main() -> None:
    con = build_db()
    for name, df in run_all(con).items():
        print(f"\n## {name}\n")
        print(df.to_markdown(index=False))


if __name__ == "__main__":
    main()
