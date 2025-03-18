# apps/core/file_management.py
from typing import Dict, List, Any, Optional, BinaryIO
from apps.core.storage.factory import StorageFactory
from apps.core.converters.factory import ConverterFactory
from apps.core.processors.factory import ProcessorFactory
from .utils.file_info import get_file_info


class FileManager:
    """Comprehensive file management system."""

    def __init__(self, storage_type: str = 'local', **storage_opts):
        """
        Initialize file manager.

        Args:
            storage_type: Type of storage to use ('local', 's3', etc.)
            **storage_opts: Options for storage initialization
        """
        self.storage = StorageFactory.get_storage(storage_type, **storage_opts)

    def upload(self, file_obj: BinaryIO, file_path: str) -> Dict[str, Any]:
        """
        Upload a file.

        Args:
            file_obj: File object to upload
            file_path: Path to save the file

        Returns:
            Dict with upload result
        """
        try:
            saved_path = self.storage.save(file_obj, file_path)

            # Get file metadata
            file_info = get_file_info(saved_path)

            return {
                "success": True,
                "path": saved_path,
                "metadata": file_info
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }