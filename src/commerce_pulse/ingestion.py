"""
Ingestion Module for CommercePulse Bronze Layer

Converts raw CSV files to Parquet format with validation, metadata tracking,
and idempotency support.
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit

from commerce_pulse.config import (
    DATASETS,
    METADATA_FILE,
    SPARK_CONFIG,
    LOG_LEVEL,
    LOG_FORMAT,
)
from commerce_pulse.data_quality import DataQualityChecker, generate_overall_quality_report, save_quality_report

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class BronzeLayerIngestion:
    """Handles ingestion of raw CSV files to Bronze Parquet layer"""

    def __init__(self):
        """Initialize Spark session and ingestion manager"""
        self.spark = self._create_spark_session()
        self.metadata = self._load_metadata()

    def _create_spark_session(self) -> SparkSession:
        """
        Create and configure Spark session

        Returns:
            Configured SparkSession
        """
        logger.info("Creating Spark session")

        builder = SparkSession.builder
        builder = builder.appName(SPARK_CONFIG["app_name"])
        builder = builder.master(SPARK_CONFIG["master"])

        # Set memory configurations
        for key, value in SPARK_CONFIG.items():
            if key.startswith("spark."):
                builder = builder.config(key, value)

        spark = builder.getOrCreate()
        logger.info(f"Spark session created: {spark.version}")
        return spark

    def _load_metadata(self) -> Dict:
        """
        Load existing metadata from file

        Returns:
            Dictionary containing metadata (empty if file doesn't exist)
        """
        if METADATA_FILE.exists():
            logger.info(f"Loading existing metadata from {METADATA_FILE}")
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        else:
            logger.info("No existing metadata found, starting fresh")
            return {"tables": {}, "last_updated": None}

    def _save_metadata(self):
        """Save current metadata to file"""
        self.metadata["last_updated"] = datetime.now().isoformat()
        with open(METADATA_FILE, "w") as f:
            json.dump(self.metadata, f, indent=2)
        logger.info(f"Metadata saved to {METADATA_FILE}")

    def _get_file_hash(self, file_path: Path) -> str:
        """
        Calculate simple hash of file based on size and modification time

        Args:
            file_path: Path to file

        Returns:
            String hash of file
        """
        stat = file_path.stat()
        return f"{stat.st_size}_{stat.st_mtime}"

    def _is_already_ingested(self, table_name: str, csv_file: Path) -> bool:
        """
        Check if table has already been ingested (idempotency check)

        Args:
            table_name: Name of the table
            csv_file: Path to source CSV file

        Returns:
            True if already ingested with same source file, False otherwise
        """
        # Check if metadata exists for this table
        if table_name not in self.metadata["tables"]:
            return False

        table_metadata = self.metadata["tables"][table_name]

        # Check if Parquet file exists
        parquet_file = DATASETS[table_name]["parquet_file"]
        if not parquet_file.exists():
            logger.info(f"Parquet file {parquet_file} does not exist, re-ingesting")
            return False

        # Check if source file has changed
        current_hash = self._get_file_hash(csv_file)
        previous_hash = table_metadata.get("source_hash")

        if current_hash != previous_hash:
            logger.info(f"Source file {csv_file} has changed, re-ingesting")
            return False

        logger.info(f"Table {table_name} already ingested (unchanged), skipping")
        return True

    def ingest_table(self, table_name: str, force: bool = False) -> Optional[Dict]:
        """
        Ingest a single table from CSV to Parquet

        Args:
            table_name: Name of the table to ingest
            force: Force re-ingestion even if already done

        Returns:
            Quality report dictionary, or None if skipped
        """
        logger.info(f"Starting ingestion for {table_name}")

        dataset_config = DATASETS[table_name]
        csv_file = dataset_config["csv_file"]
        parquet_file = dataset_config["parquet_file"]
        expected_schema = dataset_config["schema"]

        # Check if already ingested (idempotency)
        if not force and self._is_already_ingested(table_name, csv_file):
            return None

        # Check if source file exists
        if not csv_file.exists():
            logger.error(f"Source file {csv_file} does not exist")
            return None

        try:
            # Load CSV file
            logger.info(f"Loading CSV file: {csv_file}")
            df = self.spark.read.csv(str(csv_file), header=True, inferSchema=True)

            row_count = df.count()
            column_count = len(df.columns)
            logger.info(f"Loaded {row_count} rows, {column_count} columns")

            # Validate schema
            quality_checker = DataQualityChecker(table_name)
            schema_valid = quality_checker.validate_schema(df, expected_schema)

            if not schema_valid:
                logger.error(f"Schema validation failed for {table_name}")
                return None

            # Generate quality report
            quality_report = quality_checker.get_quality_report(df, expected_schema)

            # Save as Parquet
            logger.info(f"Saving to Parquet: {parquet_file}")
            df.write.mode("overwrite").parquet(str(parquet_file))

            # Calculate compression ratio
            csv_size = csv_file.stat().st_size / (1024 * 1024)  # MB
            parquet_size = sum(f.stat().st_size for f in parquet_file.parent.glob(f"{parquet_file.name}/*")) / (1024 * 1024) if parquet_file.exists() else 0
            compression_ratio = (1 - (parquet_size / csv_size)) * 100 if csv_size > 0 else 0

            # Update metadata
            self.metadata["tables"][table_name] = {
                "csv_file": str(csv_file),
                "parquet_file": str(parquet_file),
                "source_hash": self._get_file_hash(csv_file),
                "ingested_at": datetime.now().isoformat(),
                "row_count": row_count,
                "column_count": column_count,
                "csv_size_mb": round(csv_size, 2),
                "parquet_size_mb": round(parquet_size, 2),
                "compression_ratio_pct": round(compression_ratio, 2),
                "quality_score": quality_report["quality_score"],
            }

            self._save_metadata()

            logger.info(f"Successfully ingested {table_name}")
            logger.info(f"Compression: {csv_size:.2f} MB → {parquet_size:.2f} MB ({compression_ratio:.1f}% reduction)")

            return quality_report

        except Exception as e:
            logger.error(f"Error ingesting {table_name}: {str(e)}")
            raise

    def ingest_all(self, force: bool = False) -> Dict:
        """
        Ingest all tables from CSV to Parquet

        Args:
            force: Force re-ingestion of all tables

        Returns:
            Overall quality report
        """
        logger.info("=" * 60)
        logger.info("Starting Bronze Layer Ingestion for all tables")
        logger.info("=" * 60)

        quality_reports = []
        skipped_tables = []

        for table_name in DATASETS.keys():
            try:
                quality_report = self.ingest_table(table_name, force=force)

                if quality_report:
                    quality_reports.append(quality_report)
                else:
                    skipped_tables.append(table_name)

            except Exception as e:
                logger.error(f"Failed to ingest {table_name}: {str(e)}")

        # Generate overall quality report
        overall_report = generate_overall_quality_report(quality_reports)
        overall_report["skipped_tables"] = skipped_tables

        logger.info("=" * 60)
        logger.info("Bronze Layer Ingestion Complete")
        logger.info(f"Tables processed: {len(quality_reports)}")
        logger.info(f"Tables skipped: {len(skipped_tables)}")
        logger.info(f"Average quality score: {overall_report['average_quality_score']}")
        logger.info("=" * 60)

        return overall_report

    def stop(self):
        """Stop Spark session"""
        if self.spark:
            logger.info("Stopping Spark session")
            self.spark.stop()


def main():
    """Main function to run bronze layer ingestion"""
    ingestion = BronzeLayerIngestion()

    try:
        # Ingest all tables
        overall_report = ingestion.ingest_all(force=False)

        # Save quality report
        from commerce_pulse.config import QUALITY_REPORT_FILE
        save_quality_report(overall_report, QUALITY_REPORT_FILE)

        logger.info("Bronze layer ingestion completed successfully")

    except Exception as e:
        logger.error(f"Bronze layer ingestion failed: {str(e)}")
        raise

    finally:
        ingestion.stop()


if __name__ == "__main__":
    main()
