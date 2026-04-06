from __future__ import annotations

import pytest

from src.validation.validators import (
    validate_composite_uniqueness,
    validate_no_full_row_duplicates,
    validate_unique,
)


@pytest.mark.parametrize(
    "table_name,fixture_name,columns",
    [
        ("customers", "customers_df", ["customer_id"]),
        ("orders", "orders_df", ["order_id"]),
        ("products", "products_df", ["product_id"]),
    ],
)
def test_primary_key_uniqueness(table_name, fixture_name, columns, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_unique(dataframe, columns, table_name)
    assert result["passed"], result["message"]


def test_order_items_composite_key_is_unique(order_items_df):
    result = validate_composite_uniqueness(
        order_items_df, ["order_id", "order_item_id"], "order_items"
    )
    assert result["passed"], result["message"]


def test_orders_have_no_full_row_duplicates(orders_df):
    result = validate_no_full_row_duplicates(orders_df, "orders")
    assert result["passed"], result["message"]


def test_order_items_have_no_full_row_duplicates(order_items_df):
    result = validate_no_full_row_duplicates(order_items_df, "order_items")
    assert result["passed"], result["message"]
