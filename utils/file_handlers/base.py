import pandas as pd
import os
from typing import Dict, Any, Optional
import logging
import csv
from utils.file_handlers.base_handler import BaseFileHandler

logger = logging.getLogger(__name__)


class CsvHandler(BaseFileHandler):
    """
    Handler for CSV files
    """

    def read_data(self, **kwargs) -> pd.DataFrame:
        """
        Read data from CSV file

        Args:
            **kwargs: Additional parameters to pass to pd.read_csv

        Returns:
            pandas DataFrame with the data
        """
        try:
            return pd.read_csv(self.file_path, **kwargs)
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise

    def detect_delimiter(self) -> str:
        """
        Detect the delimiter used in the CSV file

        Returns:
            Detected delimiter character
        """
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as csvfile:
                # Read a small sample to detect the dialect
                sample = csvfile.read(4096)
                dialect = csv.Sniffer().sniff(sample)
                return dialect.delimiter
        except Exception as e:
            logger.warning(f"Could not detect delimiter: {str(e)}")
            return ','  # Default to comma

    def get_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata from CSV file

        Returns:
            Dictionary with metadata
        """
        try:
            delimiter = self.detect_delimiter()
            df = pd.read_csv(self.file_path, delimiter=delimiter, nrows=1)

            # Count lines in file
            with open(self.file_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)

            return {
                "file_size": self.get_file_size(),
                "delimiter": delimiter,
                "columns": df.columns.tolist(),
                "row_count": line_count - 1  # Subtract header
            }
        except Exception as e:
            logger.error(f"Error extracting CSV metadata: {str(e)}")
            raise

    def validate(self) -> Dict[str, Any]:
        """
        Validate CSV file structure and content

        Returns:
            Dictionary with validation results
        """
        try:
            delimiter = self.detect_delimiter()

            # Check if file is readable
            try:
                df = pd.read_csv(self.file_path, delimiter=delimiter)
            except Exception as e:
                return {"valid": False, "error": f"Cannot parse CSV: {str(e)}"}

            # Check if file has data
            if df.empty:
                return {"valid": False, "error": "CSV file is empty"}

            # Check for consistent row lengths
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter)
                header = next(reader)
                header_len = len(header)

                inconsistent_rows = []
                for i, row in enumerate(reader, start=2):  # Start counting from 2 (after header)
                    if len(row) != header_len:
                        inconsistent_rows.append(i)
                        if len(inconsistent_rows) >= 10:  # Limit to first 10 problems
                            break

            return {
                "valid": len(inconsistent_rows) == 0,
                "inconsistent_rows": inconsistent_rows if inconsistent_rows else None
            }
        except Exception as e:
            logger.error(f"Error validating CSV file: {str(e)}")
            return {"valid": False, "error": str(e)}


# utils/file_handlers/pdf_handler.py
import os
from typing import Dict, Any, List, Optional
import logging
import re
import pandas as pd
import PyPDF2
from utils.file_handlers.base_handler import BaseFileHandler

logger = logging.getLogger(__name__)


class PdfHandler(BaseFileHandler):
    """
    Handler for PDF files
    """

    def read_data(self) -> Dict[int, str]:
        """
        Read data from PDF file

        Returns:
            Dictionary with page numbers as keys and page text as values
        """
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                data = {}

                for i in range(len(reader.pages)):
                    page = reader.pages[i]
                    data[i + 1] = page.extract_text()

                return data
        except Exception as e:
            logger.error(f"Error reading PDF file: {str(e)}")
            raise

    def extract_tables(self) -> List[pd.DataFrame]:
        """
        Attempt to extract tables from PDF
        Note: This is a basic implementation. For production, consider 
        using specialized tools like Tabula or AWS Textract.

        Returns:
            List of pandas DataFrames with extracted tables
        """
        # This is a placeholder. For production, implement with a proper PDF table extraction tool
        logger.info("PDF table extraction would require additional specialized libraries")
        return []

    def get_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata from PDF file

        Returns:
            Dictionary with metadata
        """
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                info = reader.metadata

                metadata = {
                    "file_size": self.get_file_size(),
                    "page_count": len(reader.pages),
                    "author": info.author if hasattr(info, 'author') else None,
                    "creator": info.creator if hasattr(info, 'creator') else None,
                    "producer": info.producer if hasattr(info, 'producer') else None,
                    "subject": info.subject if hasattr(info, 'subject') else None,
                    "title": info.title if hasattr(info, 'title') else None,
                }

                return metadata
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {str(e)}")
            raise

    def validate(self) -> Dict[str, Any]:
        """
        Validate PDF file structure and content

        Returns:
            Dictionary with validation results
        """
        try:
            with open(self.file_path, 'rb') as file:
                try:
                    reader = PyPDF2.PdfReader(file)
                    page_count = len(reader.pages)

                    # Check if PDF has pages
                    if page_count == 0:
                        return {"valid": False, "error": "PDF has no pages"}

                    # Check if at least one page has text
                    has_text = False
                    for i in range(min(3, page_count)):  # Check first 3 pages
                        text = reader.pages[i].extract_text()
                        if text.strip():
                            has_text = True
                            break

                    if not has_text:
                        return {"valid": True, "warning": "PDF may be scanned or contain no text"}

                    return {"valid": True, "page_count": page_count}
                except Exception as e:
                    return {"valid": False, "error": f"Invalid PDF structure: {str(e)}"}
        except Exception as e:
            logger.error(f"Error validating PDF file: {str(e)}")
            return {"valid": False, "error": str(e)}


# utils/file_handlers/parquet_handler.py
import pandas as pd
import os
from typing import Dict, Any, Optional
import logging
from utils.file_handlers.base_handler import BaseFileHandler

logger = logging.getLogger(__name__)


class ParquetHandler(BaseFileHandler):
    """
    Handler for Parquet files
    """

    def read_data(self, **kwargs) -> pd.DataFrame:
        """
        Read data from Parquet file

        Args:
            **kwargs: Additional parameters to pass to pd.read_parquet

        Returns:
            pandas DataFrame with the data
        """
        try:
            return pd.read_parquet(self.file_path, **kwargs)
        except Exception as e:
            logger.error(f"Error reading Parquet file: {str(e)}")
            raise

    def get_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata from Parquet file

        Returns:
            Dictionary with metadata
        """
        try:
            # Read just the metadata (not loading data into memory)
            pq_metadata = pd.read_parquet(self.file_path, columns=[])

            return {
                "file_size": self.get_file_size(),
                "columns": pq_metadata.columns.tolist(),
                "row_count": len(pq_metadata),
                "memory_usage": pq_metadata.memory_usage(deep=True).sum()
            }
        except Exception as e:
            logger.error(f"Error extracting Parquet metadata: {str(e)}")
            raise

    def validate(self) -> Dict[str, Any]:
        """
        Validate Parquet file structure and content

        Returns:
            Dictionary with validation results
        """
        try:
            # Check if file is readable
            try:
                df = pd.read_parquet(self.file_path)
            except Exception as e:
                return {"valid": False, "error": f"Cannot parse Parquet file: {str(e)}"}

            # Check if file has data
            if df.empty:
                return {"valid": False, "error": "Parquet file is empty"}

            # Get basic statistics
            stats = {
                "row_count": len(df),
                "column_count": len(df.columns)
            }

            return {"valid": True, **stats}
        except Exception as e:
            logger.error(f"Error validating Parquet file: {str(e)}")
            return {"valid": False, "error": str(e)}