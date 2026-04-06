from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import BAD_DIR, get_runtime_db_path, get_runtime_raw_dir
from src.pipeline.run_pipeline import run_pipeline
from src.validation.db_utils import get_connection, read_table


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> Path:
    return run_pipeline(raw_dir=get_runtime_raw_dir())


@pytest.fixture(scope="session")
def db_path() -> Path:
    return get_runtime_db_path()


@pytest.fixture(scope="session")
def sqlite_connection(setup_database):
    connection = get_connection()
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def customers_df() -> pd.DataFrame:
    return read_table("customers")


@pytest.fixture(scope="session")
def orders_df() -> pd.DataFrame:
    return read_table("orders")


@pytest.fixture(scope="session")
def order_items_df() -> pd.DataFrame:
    return read_table("order_items")


@pytest.fixture(scope="session")
def products_df() -> pd.DataFrame:
    return read_table("products")


@pytest.fixture(scope="session")
def tables(customers_df, orders_df, order_items_df, products_df) -> dict[str, pd.DataFrame]:
    return {
        "customers": customers_df,
        "orders": orders_df,
        "order_items": order_items_df,
        "products": products_df,
    }


@pytest.fixture(scope="session")
def bad_customers_df() -> pd.DataFrame:
    return pd.read_csv(BAD_DIR / "customers.csv")


@pytest.fixture(scope="session")
def bad_orders_df() -> pd.DataFrame:
    return pd.read_csv(BAD_DIR / "orders.csv")


@pytest.fixture(scope="session")
def bad_order_items_df() -> pd.DataFrame:
    return pd.read_csv(BAD_DIR / "order_items.csv")


@pytest.fixture(scope="session")
def bad_products_df() -> pd.DataFrame:
    return pd.read_csv(BAD_DIR / "products.csv")
