# apps/core/storage/local.py
import os
from io import BytesIO
from typing import BinaryIO, Optional
from .base import StorageInterface


class LocalStorage(StorageInterface):
    """Storage implementation for local filesystem."""

    def __init__(self, base_dir: str = 'storage/'):
        """
        Initialize local storage with base directory.

        Args:
            base_dir: Base directory for file storage
        """
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def get(self, file_path: str) -> Optional[BinaryIO]:
        """
        Retrieve a file from local storage.

        Args:
            file_path: Path to the file relative to base_dir

        Returns:
            BytesIO object containing file content or None if file doesn't exist
        """
        full_path = os.path.join(self.base_dir, file_path)
        if not os.path.exists(full_path):
            return None

        with open(full_path, 'rb') as f:
            content = f.read()

        return BytesIO(content)

    def save(self, file_obj: BinaryIO, file_path: str) -> str:
        """
        Save a file to local storage.

        Args:
            file_obj: File-like object to save
            file_path: Path where to save the file relative to base_dir

        Returns:
            Path to the saved file
        """
        full_path = os.path.join(self.base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb') as f:
            for chunk in file_obj.chunks() if hasattr(file_obj, 'chunks') else [file_obj.read()]:
                f.write(chunk)

        return file_path

    def delete(self, file_path: str) -> bool:
        """
        Delete a file from local storage.

        Args:
            file_path: Path to the file to delete relative to base_dir

        Returns:
            True if deletion was successful, False otherwise
        """
        full_path = os.path.join(self.base_dir, file_path)
        if not os.path.exists(full_path):
            return False

        try:
            os.remove(full_path)
            return True
        except OSError:
            return False