from __future__ import annotations

from src.validation.schema_rules import ALLOWED_ORDER_STATUS, EXPECTED_SCHEMAS
from src.validation.validators import (
    validate_allowed_values,
    validate_columns_exist,
    validate_composite_uniqueness,
    validate_date_order,
    validate_foreign_key,
    validate_no_negative_values,
    validate_not_null,
    validate_unique,
)


def test_bad_customers_null_customer_id_is_caught(bad_customers_df):
    result = validate_not_null(bad_customers_df, "customer_id", "customers")
    assert not result["passed"]


def test_bad_customers_duplicate_customer_id_is_caught(bad_customers_df):
    result = validate_unique(bad_customers_df, ["customer_id"], "customers")
    assert not result["passed"]


def test_bad_orders_orphan_customer_is_caught(bad_orders_df, bad_customers_df):
    result = validate_foreign_key(
        bad_orders_df,
        "customer_id",
        bad_customers_df,
        "customer_id",
        "orders",
        "customers",
    )
    assert not result["passed"]


def test_bad_orders_invalid_status_is_caught(bad_orders_df):
    result = validate_allowed_values(bad_orders_df, "order_status", ALLOWED_ORDER_STATUS, "orders")
    assert not result["passed"]


def test_bad_orders_invalid_approval_date_is_caught(bad_orders_df):
    result = validate_date_order(
        bad_orders_df,
        "order_purchase_timestamp",
        "order_approved_at",
        "orders",
    )
    assert not result["passed"]


def test_bad_order_items_negative_price_is_caught(bad_order_items_df):
    result = validate_no_negative_values(bad_order_items_df, "price", "order_items")
    assert not result["passed"]


def test_bad_order_items_orphan_product_is_caught(bad_order_items_df, bad_products_df):
    result = validate_foreign_key(
        bad_order_items_df,
        "product_id",
        bad_products_df,
        "product_id",
        "order_items",
        "products",
    )
    assert not result["passed"]


def test_bad_order_items_composite_duplicate_is_caught(bad_order_items_df):
    result = validate_composite_uniqueness(
        bad_order_items_df,
        ["order_id", "order_item_id"],
        "order_items",
    )
    assert not result["passed"]


def test_bad_products_schema_mismatch_is_caught(bad_products_df):
    result = validate_columns_exist(bad_products_df, EXPECTED_SCHEMAS["products"], "products")
    assert not result["passed"]
