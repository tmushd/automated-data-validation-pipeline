from __future__ import annotations

import pytest

from src.validation.schema_rules import EXPECTED_SCHEMAS
from src.validation.validators import (
    validate_column_order,
    validate_columns_exist,
    validate_table_exists,
)


@pytest.mark.parametrize("table_name", ["customers", "orders", "order_items", "products"])
def test_tables_exist_in_sqlite(sqlite_connection, table_name):
    result = validate_table_exists(sqlite_connection, table_name)
    assert result["passed"], result["message"]


@pytest.mark.parametrize(
    "table_name,fixture_name",
    [
        ("customers", "customers_df"),
        ("orders", "orders_df"),
        ("order_items", "order_items_df"),
        ("products", "products_df"),
    ],
)
def test_expected_columns_exist(table_name, fixture_name, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_columns_exist(dataframe, EXPECTED_SCHEMAS[table_name], table_name)
    assert result["passed"], result["message"]


@pytest.mark.parametrize(
    "table_name,fixture_name",
    [
        ("customers", "customers_df"),
        ("orders", "orders_df"),
        ("order_items", "order_items_df"),
        ("products", "products_df"),
    ],
)
def test_column_order_matches_expected_schema(table_name, fixture_name, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_column_order(dataframe, EXPECTED_SCHEMAS[table_name], table_name)
    assert result["passed"], result["message"]
