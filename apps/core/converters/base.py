import logging
import os
import pandas as pd
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)


class BaseConverter:
    """Base class for all file format converters."""

    def convert(self, source_path: str, target_format: str, **kwargs) -> Optional[str]:
        """
        Convert a file from one format to another.

        Args:
            source_path: Path to the source file
            target_format: Target format ('excel', 'csv', 'parquet', etc.)
            **kwargs: Additional arguments
                - output_path: Custom output path (default: based on source_path)

        Returns:
            Path to the converted file or None if conversion failed
        """
        raise NotImplementedError("Subclasses must implement convert()")

    def _get_output_path(self, source_path: str, target_format: str, output_path: Optional[str] = None) -> str:
        """
        Generate an output path for the converted file.

        Args:
            source_path: Path to the source file
            target_format: Target format extension (e.g., '.csv', '.xlsx')
            output_path: Custom output path (optional)

        Returns:
            Path to save the converted file
        """
        if output_path:
            return output_path

        # Make sure target_format starts with a dot
        if not target_format.startswith("."):
            target_format = f".{target_format}"

        # Generate output path based on source path
        base_name = os.path.splitext(source_path)[0]
        return f"{base_name}{target_format}"

    def _read_dataframe(self, source_path: str) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame based on its extension.

        Args:
            source_path: Path to the source file

        Returns:
            DataFrame containing the file data
        """
        ext = os.path.splitext(source_path)[1].lower()

        if ext == '.csv':
            return pd.read_csv(source_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(source_path)
        elif ext == '.parquet':
            return pd.read_parquet(source_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")