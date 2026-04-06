from __future__ import annotations

import pandas as pd
import pytest

from src.validation.schema_rules import (
    ALLOWED_ORDER_STATUS,
    BLANK_STRING_COLUMNS,
    DATE_ORDER_RULES,
    NUMERIC_NON_NEGATIVE_RULES,
    ROW_COUNT_THRESHOLDS,
)
from src.validation.validators import (
    validate_allowed_values,
    validate_date_order,
    validate_min_row_count,
    validate_no_blank_strings,
    validate_no_negative_values,
)


@pytest.mark.parametrize("column", NUMERIC_NON_NEGATIVE_RULES["order_items"])
def test_order_items_numeric_fields_are_non_negative(order_items_df, column):
    result = validate_no_negative_values(order_items_df, column, "order_items")
    assert result["passed"], result["message"]


@pytest.mark.parametrize("column", NUMERIC_NON_NEGATIVE_RULES["products"])
def test_product_dimensions_are_non_negative(products_df, column):
    result = validate_no_negative_values(products_df, column, "products")
    assert result["passed"], result["message"]


def test_order_status_is_allowed(orders_df):
    result = validate_allowed_values(orders_df, "order_status", ALLOWED_ORDER_STATUS, "orders")
    assert result["passed"], result["message"]


@pytest.mark.parametrize("earlier_col,later_col", DATE_ORDER_RULES)
def test_order_dates_follow_expected_sequence(orders_df, earlier_col, later_col):
    result = validate_date_order(orders_df, earlier_col, later_col, "orders")
    assert result["passed"], result["message"]


def test_order_item_ids_start_at_one(order_items_df):
    assert pd.to_numeric(order_items_df["order_item_id"], errors="coerce").dropna().ge(1).all()


@pytest.mark.parametrize(
    "table_name,fixture_name,column",
    [
        ("customers", "customers_df", column)
        for column in BLANK_STRING_COLUMNS["customers"]
    ]
    + [("orders", "orders_df", column) for column in BLANK_STRING_COLUMNS["orders"]]
    + [
        ("order_items", "order_items_df", column)
        for column in BLANK_STRING_COLUMNS["order_items"]
    ]
    + [("products", "products_df", column) for column in BLANK_STRING_COLUMNS["products"]],
)
def test_identifier_columns_have_no_blank_strings(table_name, fixture_name, column, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_no_blank_strings(dataframe, column, table_name)
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
def test_curated_subset_meets_row_count_thresholds(table_name, fixture_name, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_min_row_count(dataframe, ROW_COUNT_THRESHOLDS[table_name], table_name)
    assert result["passed"], result["message"]
