from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
BAD_DIR = DATA_DIR / "bad"
PROCESSED_DIR = DATA_DIR / "processed"
SOURCE_FULL_DIR = DATA_DIR / "source_full"
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "pipeline.db"

TABLE_FILENAMES = {
    "customers": "customers.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "products": "products.csv",
}

SOURCE_FILENAMES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
}

TABLE_LOAD_ORDER = ["customers", "products", "orders", "order_items"]


def get_runtime_raw_dir() -> Path:
    override = os.getenv("PIPELINE_RAW_DIR")
    return Path(override).resolve() if override else RAW_DIR


def get_runtime_db_path() -> Path:
    override = os.getenv("PIPELINE_DB_PATH")
    return Path(override).resolve() if override else DB_PATH


def get_table_file_map(raw_dir: Path | None = None) -> dict[str, Path]:
    active_raw_dir = raw_dir or get_runtime_raw_dir()
    return {table: active_raw_dir / filename for table, filename in TABLE_FILENAMES.items()}
