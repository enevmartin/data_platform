import logging
import os
from typing import Optional

from .csv_processor import CSVProcessor
from .excel_processor import ExcelProcessor
from .pdf_processor import PDFProcessor
from .parquet_processor import ParquetProcessor

logger = logging.getLogger(__name__)


def get_processor_for_filetype(file_type: str):
    """
    Get the appropriate processor for the file type.

    Args:
        file_type: The type of file to process (e.g., 'csv', 'excel', 'pdf', 'parquet')

    Returns:
        Processor instance or None if no processor is found
    """
    processors = {
        'csv': CSVProcessor(),
        'excel': ExcelProcessor(),
        'pdf': PDFProcessor(),
        'parquet': ParquetProcessor(),
    }

    processor = processors.get(file_type.lower())
    if not processor:
        logger.warning(f"No processor found for file type: {file_type}")

    return processor


def get_processor_for_file(file_path: str):
    """
    Get the appropriate processor based on the file extension.

    Args:
        file_path: Path to the file

    Returns:
        Processor instance or None if no processor is found
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower().lstrip('.')

    ext_mapping = {
        'csv': 'csv',
        'xls': 'excel',
        'xlsx': 'excel',
        'xlsm': 'excel',
        'pdf': 'pdf',
        'parquet': 'parquet',
    }

    file_type = ext_mapping.get(ext)
    if not file_type:
        logger.warning(f"No processor found for file extension: {ext}")
        return None

    return get_processor_for_filetype(file_type)