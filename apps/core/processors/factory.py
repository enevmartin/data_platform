# apps/core/processors/factory.py
from typing import Dict, Any
from .base import BaseProcessor
from .csv_processor import CSVProcessor
from .excel_processor import ExcelProcessor
from .parquet_processor import ParquetProcessor
from .pdf_processor import PDFProcessor


class ProcessorFactory:
    """Factory for creating processor instances."""

    @staticmethod
    def get_processor(processor_type: str, **config) -> BaseProcessor:
        """
        Create and return a processor instance based on the specified type.

        Args:
            processor_type: Type of processor ('csv', 'excel', 'parquet', 'pdf', etc.)
            **config: Configuration parameters for the processor

        Returns:
            Appropriate BaseProcessor instance

        Raises:
            ValueError: If processor_type is not supported
        """
        if processor_type.lower() == 'csv':
            return CSVProcessor(**config)
        elif processor_type.lower() == 'excel':
            return ExcelProcessor(**config)
        elif processor_type.lower() == 'parquet':
            return ParquetProcessor(**config)
        elif processor_type.lower() == 'pdf':
            return PDFProcessor(**config)
        else:
            raise ValueError(f"Unsupported processor type: {processor_type}")