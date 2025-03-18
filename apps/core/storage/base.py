# apps/core/storage/base.py
from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, Any


class StorageInterface(ABC):
    """
    Abstract interface for storage backends.
    All storage implementations must implement these methods.
    """

    @abstractmethod
    def get(self, file_path: str) -> Optional[BinaryIO]:
        """
        Retrieve a file from storage.

        Args:
            file_path: Path to the file

        Returns:
            File-like object or None if file doesn't exist
        """
        pass

    @abstractmethod
    def save(self, file_obj: BinaryIO, file_path: str) -> str:
        """
        Save a file to storage.

        Args:
            file_obj: File-like object to save
            file_path: Path where to save the file

        Returns:
            Path to the saved file
        """
        pass

    @abstractmethod
    def delete(self, file_path: str) -> bool:
        """
        Delete a file from storage.

        Args:
            file_path: Path to the file to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        pass

# apps/core/storage/base.py (addition)
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def storage_operation(method):
    """Decorator for storage operations with error handling."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Storage operation {method.__name__} failed: {str(e)}")
            # You could also add metrics collection here
            raise
    return wrapper