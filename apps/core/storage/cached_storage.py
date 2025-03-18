# apps/core/storage/cached_storage.py
from typing import BinaryIO, Optional, Dict
from io import BytesIO
from .base import StorageInterface


class CachedStorage(StorageInterface):
    """Storage decorator that adds caching."""

    def __init__(self, storage: StorageInterface, cache_size: int = 100):
        """
        Initialize cached storage.

        Args:
            storage: Base storage implementation
            cache_size: Maximum number of files to cache
        """
        self.storage = storage
        self.cache_size = cache_size
        self.cache: Dict[str, bytes] = {}

    def get(self, file_path: str) -> Optional[BinaryIO]:
        """Get file with caching."""
        # Check cache first
        if file_path in self.cache:
            return BytesIO(self.cache[file_path])

        # Not in cache, get from storage
        file_obj = self.storage.get(file_path)
        if not file_obj:
            return None

        # Add to cache if not too big
        content = file_obj.read()
        if len(self.cache) < self.cache_size:
            self.cache[file_path] = content

        return BytesIO(content)

    def save(self, file_obj: BinaryIO, file_path: str) -> str:
        """Save file and update cache."""
        # Read content for caching
        content = file_obj.read()

        # Save to storage
        result = self.storage.save(BytesIO(content), file_path)

        # Update cache
        if len(self.cache) < self.cache_size:
            self.cache[file_path] = content

        return result

    def delete(self, file_path: str) -> bool:
        """Delete file and remove from cache."""
        # Remove from cache
        if file_path in self.cache:
            del self.cache[file_path]

        # Delete from storage
        return self.storage.delete(file_path)