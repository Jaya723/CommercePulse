"""
Data Quality Module for CommercePulse

Performs data quality checks including null analysis, duplicate detection,
schema validation, and quality scoring.
"""

import logging
from typing import Dict, List, Tuple
from datetime import datetime
import json

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, lit, sum as spark_sum

from commerce_pulse.config import QUALITY_THRESHOLDS, VALIDATION_RULES

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DataQualityChecker:
    """Performs data quality checks on PySpark DataFrames"""

    def __init__(self, table_name: str):
        """
        Initialize quality checker for a table

        Args:
            table_name: Name of the table being checked
        """
        self.table_name = table_name
        self.issues = []

    def check_nulls(self, df: DataFrame) -> Dict[str, float]:
        """
        Check null percentages for all columns

        Args:
            df: PySpark DataFrame

        Returns:
            Dictionary of column names to null percentages
        """
        logger.info(f"Checking null values for {self.table_name}")

        total_rows = df.count()
        null_percentages = {}

        for column in df.columns:
            null_count = df.filter(col(column).isNull()).count()
            null_pct = (null_count / total_rows) * 100 if total_rows > 0 else 0
            null_percentages[column] = round(null_pct, 2)

            if null_pct > QUALITY_THRESHOLDS["max_null_percentage"]:
                self.issues.append({
                    "type": "high_null_count",
                    "column": column,
                    "null_percentage": null_pct,
                    "threshold": QUALITY_THRESHOLDS["max_null_percentage"],
                })
                logger.warning(f"High null count in {column}: {null_pct}%")

        return null_percentages

    def check_duplicates(self, df: DataFrame) -> Tuple[int, float]:
        """
        Check for duplicate rows

        Args:
            df: PySpark DataFrame

        Returns:
            Tuple of (duplicate_count, duplicate_percentage)
        """
        logger.info(f"Checking duplicates for {self.table_name}")

        total_rows = df.count()
        unique_rows = df.distinct().count()
        duplicate_count = total_rows - unique_rows
        duplicate_pct = (duplicate_count / total_rows) * 100 if total_rows > 0 else 0

        if duplicate_pct > QUALITY_THRESHOLDS["max_duplicate_percentage"]:
            self.issues.append({
                "type": "duplicates_found",
                "duplicate_count": duplicate_count,
                "duplicate_percentage": duplicate_pct,
            })
            logger.warning(f"Found {duplicate_count} duplicates ({duplicate_pct}%)")

        return duplicate_count, duplicate_pct

    def validate_schema(self, df: DataFrame, expected_schema: Dict[str, str]) -> bool:
        """
        Validate DataFrame schema against expected schema

        Args:
            df: PySpark DataFrame
            expected_schema: Dictionary of column names to expected types

        Returns:
            True if schema matches, False otherwise
        """
        logger.info(f"Validating schema for {self.table_name}")

        actual_columns = set(df.columns)
        expected_columns = set(expected_schema.keys())

        # Check for missing columns
        missing_columns = expected_columns - actual_columns
        if missing_columns:
            self.issues.append({
                "type": "missing_columns",
                "columns": list(missing_columns),
            })
            logger.error(f"Missing columns: {missing_columns}")
            return False

        # Check for extra columns
        extra_columns = actual_columns - expected_columns
        if extra_columns:
            self.issues.append({
                "type": "extra_columns",
                "columns": list(extra_columns),
            })
            logger.warning(f"Extra columns found: {extra_columns}")

        return True

    def validate_business_rules(self, df: DataFrame) -> bool:
        """
        Validate business rules for the table

        Args:
            df: PySpark DataFrame

        Returns:
            True if all rules pass, False otherwise
        """
        logger.info(f"Validating business rules for {self.table_name}")

        if self.table_name not in VALIDATION_RULES:
            logger.info(f"No business rules defined for {self.table_name}")
            return True

        rules = VALIDATION_RULES[self.table_name]
        all_valid = True

        for column, valid_values in rules.items():
            if column not in df.columns:
                continue

            invalid_count = df.filter(~col(column).isin(valid_values)).count()

            if invalid_count > 0:
                self.issues.append({
                    "type": "invalid_values",
                    "column": column,
                    "invalid_count": invalid_count,
                    "valid_values": valid_values,
                })
                logger.warning(f"Found {invalid_count} invalid values in {column}")
                all_valid = False

        return all_valid

    def calculate_quality_score(self, df: DataFrame) -> float:
        """
        Calculate overall quality score (0-100)

        Args:
            df: PySpark DataFrame

        Returns:
            Quality score between 0 and 100
        """
        logger.info(f"Calculating quality score for {self.table_name}")

        null_percentages = self.check_nulls(df)
        duplicate_count, duplicate_pct = self.check_duplicates(df)

        # Calculate score based on nulls and duplicates
        avg_null_pct = sum(null_percentages.values()) / len(null_percentages) if null_percentages else 0
        score = 100 - (avg_null_pct + duplicate_pct)

        return round(max(0, min(100, score)), 2)

    def get_quality_report(self, df: DataFrame, expected_schema: Dict[str, str] = None) -> Dict:
        """
        Generate comprehensive quality report

        Args:
            df: PySpark DataFrame
            expected_schema: Expected schema (optional)

        Returns:
            Dictionary containing quality report
        """
        logger.info(f"Generating quality report for {self.table_name}")

        total_rows = df.count()
        total_columns = len(df.columns)

        null_percentages = self.check_nulls(df)
        duplicate_count, duplicate_pct = self.check_duplicates(df)

        schema_valid = True
        if expected_schema:
            schema_valid = self.validate_schema(df, expected_schema)

        business_rules_valid = self.validate_business_rules(df)

        quality_score = self.calculate_quality_score(df)

        report = {
            "table_name": self.table_name,
            "timestamp": datetime.now().isoformat(),
            "row_count": total_rows,
            "column_count": total_columns,
            "null_percentages": null_percentages,
            "duplicate_count": duplicate_count,
            "duplicate_percentage": duplicate_pct,
            "schema_valid": schema_valid,
            "business_rules_valid": business_rules_valid,
            "quality_score": quality_score,
            "issues": self.issues,
            "meets_threshold": quality_score >= QUALITY_THRESHOLDS["min_quality_score"],
        }

        return report


def generate_overall_quality_report(reports: List[Dict]) -> Dict:
    """
    Generate overall quality report across all tables

    Args:
        reports: List of individual table quality reports

    Returns:
        Dictionary containing overall quality summary
    """
    logger.info("Generating overall quality report")

    total_tables = len(reports)
    total_rows = sum(r["row_count"] for r in reports)
    avg_quality_score = sum(r["quality_score"] for r in reports) / total_tables if total_tables > 0 else 0

    tables_below_threshold = [r["table_name"] for r in reports if not r["meets_threshold"]]
    all_issues = []
    for report in reports:
        all_issues.extend(report["issues"])

    overall_report = {
        "timestamp": datetime.now().isoformat(),
        "total_tables": total_tables,
        "total_rows": total_rows,
        "average_quality_score": round(avg_quality_score, 2),
        "tables_below_threshold": tables_below_threshold,
        "total_issues": len(all_issues),
        "issues": all_issues,
        "individual_reports": reports,
    }

    return overall_report


def save_quality_report(report: Dict, output_path):
    """
    Save quality report to JSON file

    Args:
        report: Quality report dictionary
        output_path: Path to save the report
    """
    logger.info(f"Saving quality report to {output_path}")

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    logger.info("Quality report saved successfully")
