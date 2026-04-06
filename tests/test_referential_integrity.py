from __future__ import annotations

import pandas as pd
import pytest

from src.validation.validators import validate_foreign_key


@pytest.mark.parametrize(
    "child_table,child_fixture,child_col,parent_table,parent_fixture,parent_col",
    [
        ("orders", "orders_df", "customer_id", "customers", "customers_df", "customer_id"),
        ("order_items", "order_items_df", "order_id", "orders", "orders_df", "order_id"),
        ("order_items", "order_items_df", "product_id", "products", "products_df", "product_id"),
    ],
)
def test_foreign_keys_are_valid(
    child_table,
    child_fixture,
    child_col,
    parent_table,
    parent_fixture,
    parent_col,
    request,
):
    child_df = request.getfixturevalue(child_fixture)
    parent_df = request.getfixturevalue(parent_fixture)
    result = validate_foreign_key(
        child_df,
        child_col,
        parent_df,
        parent_col,
        child_table,
        parent_table,
    )
    assert result["passed"], result["message"]


def test_orders_customer_ids_map_to_exactly_one_customer_row(orders_df, customers_df):
    customer_counts = customers_df.groupby("customer_id").size()
    mapped_counts = orders_df["customer_id"].map(customer_counts)
    assert mapped_counts.eq(1).all()


def test_order_items_have_zero_orphan_orders(order_items_df, orders_df):
    orphan_count = (~order_items_df["order_id"].isin(orders_df["order_id"])) .sum()
    assert int(orphan_count) == 0


def test_order_items_have_zero_orphan_products(order_items_df, products_df):
    orphan_count = (~order_items_df["product_id"].isin(products_df["product_id"])) .sum()
    assert int(orphan_count) == 0


def test_orders_have_zero_orphan_customers(orders_df, customers_df):
    orphan_count = (~orders_df["customer_id"].isin(customers_df["customer_id"])) .sum()
    assert int(orphan_count) == 0
