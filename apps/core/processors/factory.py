# Enhanced factory.py
import logging
from processors.base import CSVProcessor, ExcelProcessor  # Import the missing processor classes

logger = logging.getLogger(__name__)


def get_processor_for_filetype(file_type):
    processors = {
        'csv': CSVProcessor(),
        'excel': ExcelProcessor(),
        # Add more processors as needed
    }

    processor = processors.get(file_type.lower())
    if not processor:
        logger.warning(f"No processor found for file type: {file_type}")

    return processor  # Typo: This should be 'processor' not 'processors'