from __future__ import annotations

import pandas as pd


DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": ["shipping_limit_date"],
}


def _trim_strings(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.select_dtypes(include=["object", "string"]).columns:
        non_null = df[column].dropna()
        df.loc[non_null.index, column] = non_null.astype(str).str.strip()
        df[column] = df[column].replace({"": pd.NA})
    return df


def _serialize_datetimes(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = _trim_strings(df.copy())

    if "customer_city" in df.columns:
        df["customer_city"] = df["customer_city"].str.lower()

    if "customer_state" in df.columns:
        df["customer_state"] = df["customer_state"].str.upper()

    if "customer_zip_code_prefix" in df.columns:
        df["customer_zip_code_prefix"] = pd.to_numeric(
            df["customer_zip_code_prefix"], errors="coerce"
        ).astype("Int64")

    return df


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = _trim_strings(df.copy())

    for identifier in ["order_id", "customer_id"]:
        if identifier in df.columns:
            df[identifier] = df[identifier].astype("string")

    if "order_status" in df.columns:
        df["order_status"] = df["order_status"].str.lower()

    return _serialize_datetimes(df, DATE_COLUMNS["orders"])


def transform_order_items(df: pd.DataFrame) -> pd.DataFrame:
    df = _trim_strings(df.copy())

    for identifier in ["order_id", "product_id", "seller_id"]:
        if identifier in df.columns:
            df[identifier] = df[identifier].astype("string")

    if "order_item_id" in df.columns:
        df["order_item_id"] = pd.to_numeric(df["order_item_id"], errors="coerce").astype(
            "Int64"
        )

    for column in ["price", "freight_value"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = _serialize_datetimes(df, DATE_COLUMNS["order_items"])

    return df


def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    df = _trim_strings(df.copy())

    if "product_id" in df.columns:
        df["product_id"] = df["product_id"].astype("string")

    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


TRANSFORMERS = {
    "customers": transform_customers,
    "orders": transform_orders,
    "order_items": transform_order_items,
    "products": transform_products,
}


def transform_data(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {
        table_name: TRANSFORMERS[table_name](df)
        for table_name, df in dataframes.items()
    }
