# Import all processors here to make them available when importing the module
from .base import BaseProcessor
from .csv_processor import CSVProcessor
from .excel_processor import ExcelProcessor
from .pdf_processor import PDFProcessor
from .parquet_processor import ParquetProcessor