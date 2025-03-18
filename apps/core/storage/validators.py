# apps/core/storage/validators.py
from typing import BinaryIO, Optional
import os


class StorageValidator:
    """Validator for storage operations."""

    @staticmethod
    def validate_file_obj(file_obj: BinaryIO) -> bool:
        """Validate file object."""
        if file_obj is None:
            return False

        # Check if file_obj has required methods
        for method in ['read', 'seek']:
            if not hasattr(file_obj, method):
                return False

        return True

    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Validate file path."""
        if not isinstance(file_path, str) or not file_path:
            return False

        # Check for directory traversal attempts
        if '..' in file_path:
            return False

        return True