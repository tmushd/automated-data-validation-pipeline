EXPECTED_SCHEMAS = {
    "customers": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "products": [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
}

NON_NULL_COLUMNS = {
    "customers": ["customer_id", "customer_unique_id"],
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "order_id",
        "order_item_id",
        "product_id",
        "price",
        "freight_value",
    ],
    "products": ["product_id"],
}

UNIQUE_RULES = {
    "customers": [["customer_id"]],
    "orders": [["order_id"]],
    "products": [["product_id"]],
    "order_items": [["order_id", "order_item_id"]],
}

FOREIGN_KEY_RULES = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
]

ALLOWED_ORDER_STATUS = {
    "created",
    "approved",
    "invoiced",
    "processing",
    "shipped",
    "delivered",
    "canceled",
    "unavailable",
}

DATE_ORDER_RULES = [
    ("order_purchase_timestamp", "order_approved_at"),
    ("order_purchase_timestamp", "order_delivered_carrier_date"),
    ("order_purchase_timestamp", "order_delivered_customer_date"),
    ("order_purchase_timestamp", "order_estimated_delivery_date"),
]

NUMERIC_NON_NEGATIVE_RULES = {
    "order_items": ["price", "freight_value"],
    "products": [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
}

DTYPE_FAMILY_RULES = {
    "customers": {
        "customer_id": "string",
        "customer_unique_id": "string",
        "customer_zip_code_prefix": "integer",
    },
    "orders": {
        "order_id": "string",
        "customer_id": "string",
        "order_purchase_timestamp": "string_datetime",
        "order_estimated_delivery_date": "string_datetime",
    },
    "order_items": {
        "order_id": "string",
        "order_item_id": "integer",
        "product_id": "string",
        "price": "numeric",
        "freight_value": "numeric",
    },
    "products": {
        "product_id": "string",
        "product_weight_g": "numeric",
        "product_length_cm": "numeric",
    },
}

ROW_COUNT_THRESHOLDS = {
    "customers": 3000,
    "orders": 3000,
    "order_items": 10000,
    "products": 3000,
}

BLANK_STRING_COLUMNS = {
    "customers": ["customer_id", "customer_unique_id"],
    "orders": ["order_id", "customer_id"],
    "order_items": ["order_id", "product_id"],
    "products": ["product_id"],
}
