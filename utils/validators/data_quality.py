# utils/validators/data_quality.py
from typing import Dict, Any, List, Optional, Set, Tuple
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DataQualityChecker:
    """
    Utility class to assess data quality and suitability for various tasks
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize with pandas DataFrame
        """
        self.df = dataframe

    def check_quality(self) -> Dict[str, Any]:
        """
        Run a full quality check on the dataframe

        Returns:
            Dictionary with quality metrics
        """
        results = {}

        # Basic stats
        results["row_count"] = len(self.df)
        results["column_count"] = len(self.df.columns)

        # Missing values check
        missing_values = self.check_missing_values()
        results["missing_values"] = missing_values
        results["has_missing_values"] = any(missing_values["missing_percentage"].values() > 0)

        # Data type check
        results["data_types"] = self.check_data_types()

        # Duplicate rows check
        duplicates = self.check_duplicates()
        results["duplicates"] = duplicates

        # Outliers check
        results["potential_outliers"] = self.check_outliers()

        # Calculate overall quality score
        results["quality_score"] = self.calculate_quality_score(results)

        # Suitability for various tasks
        suitability = self.check_suitability(results)
        results.update(suitability)

        return results

    def check_missing_values(self) -> Dict[str, Any]:
        """
        Check for missing values in the dataframe

        Returns:
            Dictionary with missing value metrics
        """
        missing_count = self.df.isnull().sum().to_dict()
        missing_percentage = (self.df.isnull().mean() * 100).to_dict()

        return {
            "missing_count": missing_count,
            "missing_percentage": missing_percentage,
            "total_missing_percentage": (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100
        }

    def check_data_types(self) -> Dict[str, str]:
        """
        Identify data types of each column

        Returns:
            Dictionary mapping column names to data types
        """
        return {col: str(dtype) for col, dtype in self.df.dtypes.to_dict().items()}

    def check_duplicates(self) -> Dict[str, Any]:
        """
        Check for duplicate rows

        Returns:
            Dictionary with duplicate metrics
        """
        duplicate_count = self.df.duplicated().sum()
        duplicate_percentage = (duplicate_count / len(self.df)) * 100 if len(self.df) > 0 else 0

        return {
            "duplicate_count": duplicate_count,
            "duplicate_percentage": duplicate_percentage
        }

    def check_outliers(self) -> Dict[str, Any]:
        """
        Check for potential outliers using IQR method

        Returns:
            Dictionary with potential outlier counts per numeric column
        """
        outliers = {}

        for col in self.df.select_dtypes(include=['int64', 'float64']).columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_count = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            outlier_percentage = (outlier_count / len(self.df)) * 100 if len(self.df) > 0 else 0

            outliers[col] = {
                "outlier_count": outlier_count,
                "outlier_percentage": outlier_percentage
            }

        return outliers

    def calculate_quality_score(self, quality_results: Dict[str, Any]) -> float:
        """
        Calculate an overall quality score (0-100)

        Args:
            quality_results: Dictionary with quality check results

        Returns:
            Quality score between 0 and 100
        """
        # Start with 100 points and deduct for issues
        score = 100.0

        # Deduct for missing values (up to 30 points)
        missing_percentage = quality_results["missing_values"]["total_missing_percentage"]
        score -= min(30, missing_percentage / 2)

        # Deduct for duplicates (up to 20 points)
        duplicate_percentage = quality_results["duplicates"]["duplicate_percentage"]
        score -= min(20, duplicate_percentage / 2)

        # Deduct for outliers (up to 20 points)
        outlier_deduction = 0
        numeric_columns = list(quality_results["potential_outliers"].keys())
        if numeric_columns:
            avg_outlier_percentage = sum(
                details["outlier_percentage"]
                for details in quality_results["potential_outliers"].values()
            ) / len(numeric_columns)
            outlier_deduction = min(20, avg_outlier_percentage / 2)
        score -= outlier_deduction

        # Ensure score is between 0 and 100
        return max(0, min(100, score))

    def check_suitability(self, quality_results: Dict[str, Any]) -> Dict[str, bool]:
        """
        Determine suitability for different tasks based on quality metrics

        Args:
            quality_results: Dictionary with quality check results

        Returns:
            Dictionary with suitability flags for different tasks
        """
        quality_score = quality_results["quality_score"]
        missing_percentage = quality_results["missing_values"]["total_missing_percentage"]

        # Determine suitability for different tasks
        suitable_for_ml = quality_score >= 70 and missing_percentage < 15
        suitable_for_visualization = quality_score >= 60

        # More sophisticated checks could be added here based on specific requirements

        return {
            "suitable_for_ml": suitable_for_ml,
            "suitable_for_visualization": suitable_for_visualization
        }

    def suggest_improvements(self) -> List[str]:
        """
        Suggest improvements to enhance data quality

        Returns:
            List of improvement suggestions
        """
        suggestions = []
        quality_results = self.check_quality()

        # Missing values suggestions
        missing_values = quality_results["missing_values"]["missing_count"]
        if any(missing_values.values()):
            columns_with_missing = [col for col, count in missing_values.items() if count > 0]
            suggestions.append(f"Consider handling missing values in columns: {', '.join(columns_with_missing)}")

            # Suggest imputation method based on data type
            for col in columns_with_missing:
                dtype = self.df[col].dtype
                if np.issubdtype(dtype, np.number):
                    suggestions.append(f"For numeric column '{col}', consider mean or median imputation")
                else:
                    suggestions.append(
                        f"For non-numeric column '{col}', consider mode imputation or a special category")

        # Duplicate suggestions
        if quality_results["duplicates"]["duplicate_count"] > 0:
            suggestions.append("Consider removing or investigating duplicate rows")

        # Outlier suggestions
        outlier_columns = [
            col for col, details in quality_results["potential_outliers"].items()
            if details["outlier_percentage"] > 5
        ]
        if outlier_columns:
            suggestions.append(f"Investigate potential outliers in columns: {', '.join(outlier_columns)}")

        # Suitability suggestions
        if not quality_results["suitable_for_ml"]:
            suggestions.append("Data requires cleaning before it's suitable for machine learning")

        return suggestions