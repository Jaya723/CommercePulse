"""
Unit tests for config module
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from commerce_pulse.config import (
    PROJECT_ROOT,
    DATA_DIR,
    RAW_DATA_DIR,
    BRONZE_DATA_DIR,
    DATASETS,
    SPARK_CONFIG,
    QUALITY_THRESHOLDS,
    VALIDATION_RULES,
)


def test_project_root_exists():
    """Test that project root directory exists"""
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()


def test_data_directories_exist():
    """Test that all data directories exist"""
    assert DATA_DIR.exists()
    assert RAW_DATA_DIR.exists()
    assert BRONZE_DATA_DIR.exists()


def test_datasets_config():
    """Test that datasets configuration is properly defined"""
    assert len(DATASETS) == 9  # 9 datasets

    # Check that each dataset has required fields
    for table_name, config in DATASETS.items():
        assert "csv_file" in config
        assert "parquet_file" in config
        assert "schema" in config
        assert isinstance(config["schema"], dict)
        assert len(config["schema"]) > 0


def test_csv_files_exist():
    """Test that all CSV files exist in raw data directory"""
    for table_name, config in DATASETS.items():
        csv_file = config["csv_file"]
        assert csv_file.exists(), f"CSV file {csv_file} does not exist for {table_name}"


def test_schema_definitions():
    """Test that schema definitions are valid"""
    for table_name, config in DATASETS.items():
        schema = config["schema"]
        for col_name, col_type in schema.items():
            assert isinstance(col_name, str)
            assert isinstance(col_type, str)
            assert col_type in ["string", "int", "float"]


def test_spark_config():
    """Test that Spark configuration is defined"""
    assert "app_name" in SPARK_CONFIG
    assert "master" in SPARK_CONFIG
    assert SPARK_CONFIG["app_name"] == "CommercePulse"


def test_quality_thresholds():
    """Test that quality thresholds are defined"""
    assert "max_null_percentage" in QUALITY_THRESHOLDS
    assert "max_duplicate_percentage" in QUALITY_THRESHOLDS
    assert "min_quality_score" in QUALITY_THRESHOLDS

    assert QUALITY_THRESHOLDS["max_null_percentage"] >= 0
    assert QUALITY_THRESHOLDS["max_null_percentage"] <= 100
    assert QUALITY_THRESHOLDS["min_quality_score"] >= 0
    assert QUALITY_THRESHOLDS["min_quality_score"] <= 100


def test_validation_rules():
    """Test that validation rules are defined"""
    assert "orders" in VALIDATION_RULES
    assert "order_payments" in VALIDATION_RULES
    assert "order_reviews" in VALIDATION_RULES

    # Check orders validation
    assert "order_status" in VALIDATION_RULES["orders"]
    assert isinstance(VALIDATION_RULES["orders"]["order_status"], list)

    # Check order_payments validation
    assert "payment_type" in VALIDATION_RULES["order_payments"]
    assert isinstance(VALIDATION_RULES["order_payments"]["payment_type"], list)

    # Check order_reviews validation
    assert "review_score" in VALIDATION_RULES["order_reviews"]
    assert isinstance(VALIDATION_RULES["order_reviews"]["review_score"], list)


def test_parquet_file_paths():
    """Test that Parquet file paths are in bronze directory"""
    for table_name, config in DATASETS.items():
        parquet_file = config["parquet_file"]
        assert BRONZE_DATA_DIR in parquet_file.parents
        assert parquet_file.suffix == ".parquet"
