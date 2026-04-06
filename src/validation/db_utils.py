from __future__ import annotations

import sqlite3

import pandas as pd

from src.config import get_runtime_db_path


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_runtime_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def read_table(table_name: str) -> pd.DataFrame:
    with get_connection() as connection:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)


def get_table_names() -> list[str]:
    with get_connection() as connection:
        results = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
            connection,
        )
    return results["name"].tolist()
