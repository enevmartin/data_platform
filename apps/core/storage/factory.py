# apps/core/storage/factory.py
from typing import Dict, Any
from .base import StorageInterface
from .local import LocalStorage
from .s3 import S3Storage


class StorageFactory:
    """Factory for creating storage instances."""

    @staticmethod
    def get_storage(storage_type: str, **storage_opts) -> StorageInterface:
        """
        Create and return a storage instance based on the specified type.

        Args:
            storage_type: Type of storage ('local', 's3', etc.)
            **storage_opts: Configuration parameters for the storage

        Returns:
            Appropriate StorageInterface instance

        Raises:
            ValueError: If storage_type is not supported
        """
        if storage_type.lower() == 'local':
            return LocalStorage(**storage_opts)
        elif storage_type.lower() == 's3':
            return S3Storage(**storage_opts)
        elif storage_type.lower() == 'cached':
            from .cached_storage import CachedStorage
            return CachedStorage(**storage_opts)
        elif storage_type.lower() == 'encrypted':
            from .encrypted_storage import EncryptedStorage
            return EncryptedStorage(**storage_opts)
        elif storage_type.lower() == 'async':
            from .async_storage import AsyncStorage
            return AsyncStorage(**storage_opts)
        elif storage_type.lower() == 'media':
            from .media_storage import MediaStorage
            return MediaStorage(**storage_opts)
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")