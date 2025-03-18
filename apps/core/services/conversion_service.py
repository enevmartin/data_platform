# apps/core/services/conversion_service.py
from typing import Optional
from apps.core.storage.factory import StorageFactory
from ..converters.factory import ConverterFactory


class ConversionService:
    """Service for handling file conversions with storage."""

    def __init__(self, source_storage_type='local', target_storage_type='local'):
        self.source_storage = StorageFactory.get_storage(source_storage_type)
        self.target_storage = StorageFactory.get_storage(target_storage_type)

    def convert_file(self, source_path: str, target_format: str) -> Optional[str]:
        """
        Convert a file from source path to target format.

        Args:
            source_path: Path to source file in source storage
            target_format: Target file format (e.g., 'csv', 'excel')

        Returns:
            Path to converted file in target storage or None if conversion failed
        """
        # Get source file
        source_file = self.source_storage.get(source_path)
        if not source_file:
            return None

        # Determine source format
        source_format = source_path.split('.')[-1].lower()

        # Get converter
        converter = ConverterFactory.get_converter(source_format)
        if not converter:
            return None

        # Convert file
        target_path = source_path.rsplit('.', 1)[0] + '.' + target_format
        converted_file = converter.convert(source_file, target_format)

        # Save converted file
        if converted_file:
            return self.target_storage.save(converted_file, target_path)

        return None