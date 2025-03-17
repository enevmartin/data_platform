import logging
import pandas as pd
import os
from typing import Dict, Any, Optional

from .base import BaseProcessor

logger = logging.getLogger(__name__)


class ExcelProcessor(BaseProcessor):
    """Processor for Excel files (XLS, XLSX)."""

    def _process_file(self, datafile) -> None:
        """Process an Excel file."""
        file_path = datafile.file.path
        logger.info(f"Processing Excel file: {file_path}")

        try:
            # Example processing - read the Excel file
            df = pd.read_excel(file_path)

            # Perform any processing you need
            # For example, data cleaning, transformation, etc.

            # You might want to save processed data to a new file format like CSV
            processed_path = f"{os.path.splitext(file_path)[0]}.csv"
            df.to_csv(processed_path, index=False)
            datafile.processed_file = processed_path
            datafile.save(update_fields=['processed_file'])

            # Example: Store summary statistics
            stats = df.describe().to_dict()
            datafile.statistics = stats
            datafile.save(update_fields=['statistics'])

        except Exception as e:
            logger.exception(f"Error processing Excel file {file_path}")
            raise

    def validate(self, datafile) -> Dict[str, Any]:
        """Validate that the file is a valid Excel file."""
        try:
            # Check file extension
            if not any(datafile.file.name.lower().endswith(ext) for ext in ['.xls', '.xlsx', '.xlsm']):
                return {'is_valid': False, 'message': 'File is not an Excel file'}

            # Try to read with pandas
            df = pd.read_excel(datafile.file.path)

            # Check if file has data
            if df.empty:
                return {'is_valid': False, 'message': 'Excel file is empty'}

            return {'is_valid': True, 'message': 'Valid Excel file'}
        except Exception as e:
            return {'is_valid': False, 'message': f'Invalid Excel file: {str(e)}'}

    def extract_metadata(self, datafile) -> Optional[Dict[str, Any]]:
        """Extract metadata from the Excel file."""
        try:
            # Get sheet names
            excel_file = pd.ExcelFile(datafile.file.path)
            sheet_names = excel_file.sheet_names

            # Read first sheet for basic metadata
            df = pd.read_excel(datafile.file.path, sheet_name=sheet_names[0])

            metadata = {
                'sheet_count': len(sheet_names),
                'sheet_names': sheet_names,
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': list(df.columns),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }

            # Add sample data (first 5 rows of first sheet)
            metadata['sample'] = df.head(5).to_dict('records')

            # Add basic info about other sheets
            metadata['sheets_info'] = {}
            for sheet in sheet_names:
                sheet_df = pd.read_excel(datafile.file.path, sheet_name=sheet)
                metadata['sheets_info'][sheet] = {
                    'row_count': len(sheet_df),
                    'column_count': len(sheet_df.columns)
                }

            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata from Excel: {str(e)}")
            return None