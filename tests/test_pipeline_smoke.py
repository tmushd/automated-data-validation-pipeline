from __future__ import annotations

import pytest

from src.pipeline.run_pipeline import run_pipeline
from src.validation.db_utils import get_table_names
from src.validation.validators import validate_non_empty_dataframe


EXPECTED_TABLES = {"customers", "orders", "order_items", "products"}


def test_database_file_exists(db_path):
    assert db_path.exists()


def test_pipeline_run_completes_without_exception():
    assert run_pipeline().exists()


def test_expected_tables_exist():
    assert EXPECTED_TABLES.issubset(set(get_table_names()))


@pytest.mark.parametrize(
    "table_name,fixture_name",
    [
        ("customers", "customers_df"),
        ("orders", "orders_df"),
        ("order_items", "order_items_df"),
        ("products", "products_df"),
    ],
)
def test_loaded_tables_are_non_empty(table_name, fixture_name, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_non_empty_dataframe(dataframe, table_name)
    assert result["passed"], result["message"]
