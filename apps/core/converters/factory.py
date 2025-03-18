# apps/core/converters/factory.py
from typing import Dict, Any
from .base import BaseConverter
from .csv_converter import CSVConverter
from .excel_converter import ExcelConverter


class ConverterFactory:
    """Factory for creating converter instances."""

    @staticmethod
    def get_converter(converter_type: str, **config) -> BaseConverter:
        """
        Create and return a converter instance based on the specified type.

        Args:
            converter_type: Type of converter ('csv', 'excel', etc.)
            **config: Configuration parameters for the converter

        Returns:
            Appropriate BaseConverter instance

        Raises:
            ValueError: If converter_type is not supported
        """
        if converter_type.lower() == 'csv':
            return CSVConverter(**config)
        elif converter_type.lower() == 'excel':
            return ExcelConverter(**config)
        else:
            raise ValueError(f"Unsupported converter type: {converter_type}")