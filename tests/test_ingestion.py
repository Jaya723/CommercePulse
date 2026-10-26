"""
Unit tests for ingestion module
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from commerce_pulse.ingestion import BronzeLayerIngestion
from commerce_pulse.config import DATASETS, METADATA_FILE


@pytest.fixture
def ingestion():
    """Create a BronzeLayerIngestion instance for testing"""
    with patch('commerce_pulse.ingestion.SparkSession') as mock_spark:
        mock_session = Mock()
        mock_spark.builder.appName.return_value.master.return_value.config.return_value.getOrCreate.return_value = mock_session
        mock_session.version = "3.5.0"

        ingestion = BronzeLayerIngestion()
        ingestion.spark = mock_session

        yield ingestion

        ingestion.stop()


def test_ingestion_initialization(ingestion):
    """Test that ingestion initializes correctly"""
    assert ingestion.spark is not None
    assert ingestion.metadata is not None
    assert "tables" in ingestion.metadata


def test_create_spark_session():
    """Test Spark session creation"""
    with patch('commerce_pulse.ingestion.SparkSession') as mock_spark:
        mock_session = Mock()
        # Mock the builder chain properly
        mock_builder = Mock()
        mock_spark.builder = mock_builder
        mock_builder.appName.return_value = mock_builder
        mock_builder.master.return_value = mock_builder
        mock_builder.config.return_value = mock_builder
        mock_builder.getOrCreate.return_value = mock_session
        mock_session.version = "3.5.0"

        ingestion = BronzeLayerIngestion()

        assert ingestion.spark == mock_session
        mock_builder.appName.assert_called_once()
        mock_builder.master.assert_called_once()

        ingestion.stop()


def test_load_metadata_no_file(ingestion):
    """Test metadata loading when file doesn't exist"""
    # Mock metadata file not existing
    with patch('commerce_pulse.ingestion.METADATA_FILE', Path("nonexistent_file.json")):
        ingestion.metadata = ingestion._load_metadata()

    assert ingestion.metadata == {"tables": {}, "last_updated": None}


def test_load_metadata_with_file(ingestion, tmp_path):
    """Test metadata loading when file exists"""
    # Create temporary metadata file
    metadata_file = tmp_path / "metadata.json"
    test_metadata = {
        "tables": {"customers": {"ingested_at": "2024-01-01"}},
        "last_updated": "2024-01-01T00:00:00"
    }

    with open(metadata_file, "w") as f:
        json.dump(test_metadata, f)

    with patch('commerce_pulse.ingestion.METADATA_FILE', metadata_file):
        ingestion.metadata = ingestion._load_metadata()

    assert ingestion.metadata == test_metadata


def test_save_metadata(ingestion, tmp_path):
    """Test metadata saving"""
    metadata_file = tmp_path / "metadata.json"

    with patch('commerce_pulse.ingestion.METADATA_FILE', metadata_file):
        ingestion.metadata = {"tables": {}, "last_updated": None}
        ingestion._save_metadata()

    assert metadata_file.exists()
    with open(metadata_file, "r") as f:
        saved_metadata = json.load(f)

    assert "last_updated" in saved_metadata
    assert saved_metadata["last_updated"] is not None


def test_get_file_hash(ingestion):
    """Test file hash calculation"""
    # Create a temporary file
    test_file = Path("test_file.txt")
    test_file.write_text("test content")

    try:
        hash_value = ingestion._get_file_hash(test_file)
        assert isinstance(hash_value, str)
        assert "_" in hash_value  # Format: size_mtime
    finally:
        test_file.unlink()


def test_is_already_ingested_false(ingestion):
    """Test idempotency check when table not ingested"""
    table_name = "customers"
    csv_file = DATASETS[table_name]["csv_file"]

    result = ingestion._is_already_ingested(table_name, csv_file)

    assert result is False


def test_is_already_ingested_true(ingestion, tmp_path):
    """Test idempotency check when table already ingested"""
    table_name = "customers"
    csv_file = DATASETS[table_name]["csv_file"]

    # Mock metadata as if already ingested
    ingestion.metadata["tables"][table_name] = {
        "source_hash": ingestion._get_file_hash(csv_file),
        "ingested_at": "2024-01-01T00:00:00"
    }

    # Mock parquet file existence
    with patch.object(Path, 'exists', return_value=True):
        result = ingestion._is_already_ingested(table_name, csv_file)

    assert result is True


def test_ingest_table_skipped(ingestion):
    """Test table ingestion when already ingested (idempotency)"""
    table_name = "customers"
    csv_file = DATASETS[table_name]["csv_file"]

    # Mock as already ingested
    ingestion.metadata["tables"][table_name] = {
        "source_hash": ingestion._get_file_hash(csv_file),
        "ingested_at": "2024-01-01T00:00:00"
    }

    with patch.object(Path, 'exists', return_value=True):
        result = ingestion.ingest_table(table_name, force=False)

    assert result is None  # Skipped


def test_ingest_table_source_not_exists(ingestion):
    """Test table ingestion when source file doesn't exist"""
    table_name = "customers"

    with patch.object(Path, 'exists', return_value=False):
        result = ingestion.ingest_table(table_name, force=True)

    assert result is None


def test_ingest_table_success(ingestion, tmp_path):
    """Test successful table ingestion"""
    table_name = "customers"
    dataset_config = DATASETS[table_name]

    # Mock DataFrame
    mock_df = Mock()
    mock_df.count.return_value = 100
    mock_df.columns = ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"]

    # Mock Spark read
    ingestion.spark.read.csv.return_value = mock_df

    # Mock quality checker to avoid PySpark issues
    mock_quality_report = {
        "table_name": "customers",
        "row_count": 100,
        "column_count": 5,
        "quality_score": 95.0,
        "meets_threshold": True,
        "issues": [],
    }

    # Mock file operations
    with patch('commerce_pulse.ingestion.DataQualityChecker') as mock_checker_class:
        mock_checker = Mock()
        mock_checker_class.return_value = mock_checker
        mock_checker.get_quality_report.return_value = mock_quality_report

        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'stat') as mock_stat:
                mock_stat.return_value.st_size = 1000000
                mock_stat.return_value.st_mtime = 1234567890

                # Mock parquet write
                mock_df.write.mode.return_value.parquet.return_value = None

                # Mock parquet file size calculation
                with patch('commerce_pulse.ingestion.Path.glob', return_value=[]):
                    result = ingestion.ingest_table(table_name, force=True)

    assert result is not None
    assert "quality_score" in result
    assert table_name in ingestion.metadata["tables"]


def test_ingest_all(ingestion):
    """Test ingestion of all tables"""
    # Mock individual table ingestion
    with patch.object(ingestion, 'ingest_table') as mock_ingest:
        mock_ingest.return_value = {
            "quality_score": 90,
            "table_name": "test",
            "row_count": 100,
            "meets_threshold": True,
            "issues": [],
        }

        result = ingestion.ingest_all(force=True)

    assert "average_quality_score" in result
    assert "total_tables" in result
    assert "individual_reports" in result


def test_stop(ingestion):
    """Test Spark session stop"""
    ingestion.stop()
    ingestion.spark.stop.assert_called_once()
