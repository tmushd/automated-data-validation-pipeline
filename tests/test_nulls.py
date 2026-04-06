from __future__ import annotations

import pytest

from src.validation.validators import validate_not_null


NON_NULL_CASES = [
    ("customers", "customers_df", "customer_id"),
    ("customers", "customers_df", "customer_unique_id"),
    ("orders", "orders_df", "order_id"),
    ("orders", "orders_df", "customer_id"),
    ("orders", "orders_df", "order_status"),
    ("orders", "orders_df", "order_purchase_timestamp"),
    ("orders", "orders_df", "order_estimated_delivery_date"),
    ("order_items", "order_items_df", "order_id"),
    ("order_items", "order_items_df", "order_item_id"),
    ("order_items", "order_items_df", "product_id"),
]


@pytest.mark.parametrize("table_name,fixture_name,column", NON_NULL_CASES)
def test_required_columns_are_not_null(table_name, fixture_name, column, request):
    dataframe = request.getfixturevalue(fixture_name)
    result = validate_not_null(dataframe, column, table_name)
    assert result["passed"], result["message"]
