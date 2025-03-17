import logging
import os
import pandas as pd
from typing import Dict, Optional

from .base import BaseConverter

logger = logging.getLogger(__name__)


class CSVConverter(BaseConverter):
    """Converter for CSV files."""

    def convert(self, source_path: str, target_format: str, **kwargs) -> Optional[str]:
        """
        Convert a CSV file to another format.

        Args:
            source_path: Path to the CSV file
            target_format: Target format ('excel', 'parquet')
            **kwargs: Additional arguments
                - output_path: Custom output path (default: based on source_path)
                - excel_sheet_name: Sheet name for Excel output (default: 'Sheet1')

        Returns:
            Path to the converted file or None if conversion failed
        """
        try:
            output_path = kwargs.get('output_path')

            # Read CSV file
            df = pd.read_csv(source_path)

            # Determine output path if not provided
            if not output_path:
                base_path = os.path.splitext(source_path)[0]
                if target_format == 'excel':
                    output_path = f"{base_path}.xlsx"
                else:
                    output_path = f"{base_path}.{target_format}"

            # Convert to target format
            if target_format == 'excel':
                sheet_name = kwargs.get('excel_sheet_name', 'Sheet1')
                df.to_excel(output_path, sheet_name=sheet_name, index=False)
            elif target_format == 'parquet':
                df.to_parquet(output_path, index=False)
            else:
                logger.warning(f"Unsupported target format: {target_format}")
                return None

            return output_path
        except Exception as e:
            logger.exception(f"Error converting CSV file {source_path} to {target_format}")
            return None

    def supported_formats(self) -> Dict[str, list]:
        """Return supported formats."""
        return {
            'from': ['csv'],
            'to': ['excel', 'parquet']
        }