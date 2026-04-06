from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.config import DB_DIR, PROCESSED_DIR, TABLE_LOAD_ORDER, get_runtime_db_path
from src.utils.logger import get_logger

logger = get_logger(__name__)

CREATE_TABLE_STATEMENTS = {
    "customers": """
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            customer_unique_id TEXT NOT NULL,
            customer_zip_code_prefix INTEGER,
            customer_city TEXT,
            customer_state TEXT
        )
    """,
    "products": """
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_category_name TEXT,
            product_name_lenght REAL,
            product_description_lenght REAL,
            product_photos_qty REAL,
            product_weight_g REAL,
            product_length_cm REAL,
            product_height_cm REAL,
            product_width_cm REAL
        )
    """,
    "orders": """
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_status TEXT NOT NULL,
            order_purchase_timestamp TEXT NOT NULL,
            order_approved_at TEXT,
            order_delivered_carrier_date TEXT,
            order_delivered_customer_date TEXT,
            order_estimated_delivery_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """,
    "order_items": """
        CREATE TABLE order_items (
            order_id TEXT NOT NULL,
            order_item_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            seller_id TEXT,
            shipping_limit_date TEXT,
            price REAL NOT NULL,
            freight_value REAL NOT NULL,
            PRIMARY KEY (order_id, order_item_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """,
}


def _prepare_for_sqlite(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    for column in prepared.columns:
        if pd.api.types.is_datetime64_any_dtype(prepared[column]):
            prepared[column] = prepared[column].dt.strftime("%Y-%m-%d %H:%M:%S")
        prepared[column] = prepared[column].where(prepared[column].notna(), None)
    return prepared


def _write_processed_csvs(dataframes: dict[str, pd.DataFrame]) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for table_name, df in dataframes.items():
        df.to_csv(PROCESSED_DIR / f"{table_name}.csv", index=False)


def load_to_sqlite(
    dataframes: dict[str, pd.DataFrame], db_path: Path | None = None
) -> Path:
    target_db_path = db_path or get_runtime_db_path()
    DB_DIR.mkdir(parents=True, exist_ok=True)
    _write_processed_csvs(dataframes)
    if target_db_path.exists():
        target_db_path.unlink()

    with sqlite3.connect(target_db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        for table_name in TABLE_LOAD_ORDER:
            logger.info("Creating table %s", table_name)
            connection.execute(CREATE_TABLE_STATEMENTS[table_name])
            prepared_df = _prepare_for_sqlite(dataframes[table_name])
            logger.info("Loading %s rows into %s", len(prepared_df), table_name)
            prepared_df.to_sql(table_name, connection, if_exists="append", index=False)
        connection.commit()

    logger.info("SQLite database created at %s", target_db_path)
    return target_db_path
