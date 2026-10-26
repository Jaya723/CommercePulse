"""
Configuration module for CommercePulse

Centralized configuration for paths, schemas, and Spark settings.
Supports environment variable overrides for Colab execution.
"""

import os
from pathlib import Path
from typing import Dict, List

# Project root directory - can be overridden via environment variable
PROJECT_ROOT = Path(os.environ.get("COMMERCE_PULSE_ROOT", Path(__file__).parent.parent.parent))

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
BRONZE_DATA_DIR = DATA_DIR / "bronze"
SILVER_DATA_DIR = DATA_DIR / "silver"
GOLD_DATA_DIR = DATA_DIR / "gold"
QUALITY_DIR = DATA_DIR / "quality"
METRICS_DIR = DATA_DIR / "metrics"

# Ensure directories exist
for dir_path in [RAW_DATA_DIR, BRONZE_DATA_DIR, SILVER_DATA_DIR, GOLD_DATA_DIR, QUALITY_DIR, METRICS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Dataset file definitions
DATASETS = {
    "customers": {
        "csv_file": RAW_DATA_DIR / "olist_customers_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "customers.parquet",
        "schema": {
            "customer_id": "string",
            "customer_unique_id": "string",
            "customer_zip_code_prefix": "int",
            "customer_city": "string",
            "customer_state": "string",
        },
    },
    "geolocation": {
        "csv_file": RAW_DATA_DIR / "olist_geolocation_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "geolocation.parquet",
        "schema": {
            "geolocation_zip_code_prefix": "int",
            "geolocation_lat": "float",
            "geolocation_lng": "float",
            "geolocation_city": "string",
            "geolocation_state": "string",
        },
    },
    "order_items": {
        "csv_file": RAW_DATA_DIR / "olist_order_items_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "order_items.parquet",
        "schema": {
            "order_id": "string",
            "order_item_id": "int",
            "product_id": "string",
            "seller_id": "string",
            "shipping_limit_date": "string",
            "price": "float",
            "freight_value": "float",
        },
    },
    "order_payments": {
        "csv_file": RAW_DATA_DIR / "olist_order_payments_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "order_payments.parquet",
        "schema": {
            "order_id": "string",
            "payment_sequential": "int",
            "payment_type": "string",
            "payment_installments": "int",
            "payment_value": "float",
        },
    },
    "order_reviews": {
        "csv_file": RAW_DATA_DIR / "olist_order_reviews_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "order_reviews.parquet",
        "schema": {
            "review_id": "string",
            "order_id": "string",
            "review_score": "int",
            "review_comment_title": "string",
            "review_comment_message": "string",
            "review_creation_date": "string",
            "review_answer_timestamp": "string",
        },
    },
    "orders": {
        "csv_file": RAW_DATA_DIR / "olist_orders_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "orders.parquet",
        "schema": {
            "order_id": "string",
            "customer_id": "string",
            "order_status": "string",
            "order_purchase_timestamp": "string",
            "order_approved_at": "string",
            "order_delivered_carrier_date": "string",
            "order_delivered_customer_date": "string",
            "order_estimated_delivery_date": "string",
        },
    },
    "products": {
        "csv_file": RAW_DATA_DIR / "olist_products_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "products.parquet",
        "schema": {
            "product_id": "string",
            "product_category_name": "string",
            "product_name_lenght": "float",
            "product_description_lenght": "float",
            "product_photos_qty": "float",
            "product_weight_g": "float",
            "product_length_cm": "float",
            "product_height_cm": "float",
            "product_width_cm": "float",
        },
    },
    "sellers": {
        "csv_file": RAW_DATA_DIR / "olist_sellers_dataset.csv",
        "parquet_file": BRONZE_DATA_DIR / "sellers.parquet",
        "schema": {
            "seller_id": "string",
            "seller_zip_code_prefix": "int",
            "seller_city": "string",
            "seller_state": "string",
        },
    },
    "category_translation": {
        "csv_file": RAW_DATA_DIR / "product_category_name_translation.csv",
        "parquet_file": BRONZE_DATA_DIR / "category_translation.parquet",
        "schema": {
            "product_category_name": "string",
            "product_category_name_english": "string",
        },
    },
}

# Metadata file
METADATA_FILE = BRONZE_DATA_DIR / "metadata.json"

# Quality report file
QUALITY_REPORT_FILE = QUALITY_DIR / "quality_report.json"

# Spark configuration
SPARK_CONFIG = {
    "app_name": "CommercePulse",
    "master": "local[*]",  # Use all available cores
    "spark.driver.memory": "4g",
    "spark.executor.memory": "4g",
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
}

# Data quality thresholds
QUALITY_THRESHOLDS = {
    "max_null_percentage": 5.0,  # Maximum allowed null percentage
    "max_duplicate_percentage": 0.0,  # Duplicates not allowed
    "min_quality_score": 70.0,  # Minimum acceptable quality score
}

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Business validation rules
VALIDATION_RULES = {
    "orders": {
        "order_status": ["created", "approved", "invoiced", "shipped", "delivered", "canceled", "unavailable", "processing"],
    },
    "order_payments": {
        "payment_type": ["credit_card", "boleto", "voucher", "debit_card"],
    },
    "order_reviews": {
        "review_score": [1, 2, 3, 4, 5],
    },
}
