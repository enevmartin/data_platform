import logging
import pandas as pd
import os
from typing import Dict, Any, Optional

from .base import BaseProcessor

logger = logging.getLogger(__name__)


class ParquetProcessor(BaseProcessor):
    """Processor for Parquet files."""

    def _process_file(self, datafile) -> None:
        """Process a Parquet file."""
        file_path = datafile.file.path
        logger.info(f"Processing Parquet file: {file_path}")

        try:
            # Example processing - read the Parquet file
            df = pd.read_parquet(file_path)

            # Perform any processing you need
            # For example, data cleaning, transformation, etc.

            # Example: Convert to CSV for easier access if needed
            csv_path = f"{os.path.splitext(file_path)[0]}.csv"
            df.to_csv(csv_path, index=False)

            # Update datafile with processed file path
            datafile.processed_file = csv_path
            datafile.save(update_fields=['processed_file'])

            # Example: Store summary statistics
            stats = df.describe().to_dict()
            datafile.statistics = stats
            datafile.save(update_fields=['statistics'])

        except Exception as e:
            logger.exception(f"Error processing Parquet file {file_path}")
            raise

    def validate(self, datafile) -> Dict[str, Any]:
        """Validate that the file is a valid Parquet file."""
        try:
            # Check file extension
            if not datafile.file.name.lower().endswith('.parquet'):
                return {'is_valid': False, 'message': 'File is not a Parquet file'}

            # Try to read with pandas
            df = pd.read_parquet(datafile.file.path)

            # Check if file has data
            if df.empty:
                return {'is_valid': False, 'message': 'Parquet file is empty'}

            return {'is_valid': True, 'message': 'Valid Parquet file'}
        except Exception as e:
            return {'is_valid': False, 'message': f'Invalid Parquet file: {str(e)}'}

    def extract_metadata(self, datafile) -> Optional[Dict[str, Any]]:
        """Extract metadata from the Parquet file."""
        try:
            df = pd.read_parquet(datafile.file.path)
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
            logger.error(f"Error extracting metadata from Parquet: {str(e)}")
            return None