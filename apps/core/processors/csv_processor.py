import logging
import pandas as pd
import os
from typing import Dict, Any, Optional

from .base import BaseProcessor

logger = logging.getLogger(__name__)


class CSVProcessor(BaseProcessor):
    """Processor for CSV files."""

    def _process_file(self, datafile) -> None:
        """Process a CSV file."""
        file_path = datafile.file.path
        logger.info(f"Processing CSV file: {file_path}")

        try:
            # Example processing - read the CSV file
            df = pd.read_csv(file_path)

            # Perform any processing you need
            # For example, data cleaning, transformation, etc.

            # You might want to save processed data to a new file
            # processed_path = f"{os.path.splitext(file_path)[0]}_processed.csv"
            # df.to_csv(processed_path, index=False)
            # datafile.processed_file = processed_path
            # datafile.save(update_fields=['processed_file'])

            # Example: Store summary statistics
            stats = df.describe().to_dict()
            datafile.statistics = stats
            datafile.save(update_fields=['statistics'])

        except Exception as e:
            logger.exception(f"Error processing CSV file {file_path}")
            raise

    def validate(self, datafile) -> Dict[str, Any]:
        """Validate that the file is a valid CSV."""
        try:
            # Check file extension
            if not datafile.file.name.lower().endswith('.csv'):
                return {'is_valid': False, 'message': 'File is not a CSV'}

            # Try to read with pandas
            df = pd.read_csv(datafile.file.path)

            # Check if file has data
            if df.empty:
                return {'is_valid': False, 'message': 'CSV file is empty'}

            return {'is_valid': True, 'message': 'Valid CSV file'}
        except Exception as e:
            return {'is_valid': False, 'message': f'Invalid CSV file: {str(e)}'}

    def extract_metadata(self, datafile) -> Optional[Dict[str, Any]]:
        """Extract metadata from the CSV file."""
        try:
            df = pd.read_csv(datafile.file.path)
            metadata = {
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': list(df.columns),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }

            # Add sample data (first 5 rows)
            metadata['sample'] = df.head(5).to_dict('records')

            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata from CSV: {str(e)}")
            return None