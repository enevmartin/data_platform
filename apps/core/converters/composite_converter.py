# apps/core/converters/composite_converter.py
from typing import List, BinaryIO, Optional
from apps.core.converters.base import BaseConverter


class CompositeConverter(BaseConverter):
    """Combines multiple converters into a single conversion pipeline."""

    def __init__(self, converters: List[BaseConverter]):
        """Initialize with a list of converters."""
        self.converters = converters

    def convert(self, file_obj: BinaryIO, target_format: str) -> Optional[BinaryIO]:
        """
        Convert file through multiple converters.

        Args:
            file_obj: Source file object
            target_format: Final target format

        Returns:
            Converted file object or None if conversion failed
        """
        current_obj = file_obj
        for converter in self.converters:
            if current_obj is None:
                return None

            current_obj = converter.convert(current_obj, target_format)

        return current_obj