import logging
import os
import pandas as pd
from typing import Dict, Optional

from .base import BaseConverter

logger = logging.getLogger(__name__)


class ExcelConverter(BaseConverter):
    """Converter for Excel files."""

    def convert(self, source_path: str, target_format: str, **kwargs) -> Optional[str]:
        """
        Convert an Excel file to another format.

        Args:
            source_path: Path to the Excel file
            target_format: Target format ('csv', 'parquet')
            **kwargs: Additional arguments
                - sheet_name: Name or index of the sheet to convert (default: 0)
                - output_path: Custom output path (default: based on source_path)

        Returns:
            Path to the converted file or None if conversion failed
        """
        try:
            sheet_name = kwargs.get('sheet_name', 0)
            output_path = kwargs.get('output_path')

            # Read Excel file
            df = pd.read_excel(source_path, sheet_name=sheet_name)

            # Determine output path if not provided
            if not output_path:
                base_path = os.path.splitext(source_path)[0]
                output_path = f"{base_path}.{target_format}"

            # Convert to target format
            if target_format == 'csv':
                df.to_csv(output_path, index=False)
            elif target_format == 'parquet':
                df.to_parquet(output_path, index=False)
            else:
                logger.warning(f"Unsupported target format: {target_format}")
                return None

            return output_path
        except Exception as e:
            logger.exception(f"Error converting Excel file {source_path} to {target_format}")
            return None

    def supported_formats(self) -> Dict[str, list]:
        """Return supported formats."""
        return {
            'from': ['excel'],
            'to': ['csv', 'parquet']
        }