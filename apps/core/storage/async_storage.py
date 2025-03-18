# apps/core/storage/async_storage.py
import asyncio
from typing import BinaryIO, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
from .base import StorageInterface


class AsyncStorageWrapper:
    """Async wrapper for synchronous storage implementations."""

    def __init__(self, storage: StorageInterface, max_workers: int = 5):
        self.storage = storage
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def get(self, file_path: str) -> Optional[BinaryIO]:
        """Async version of get."""
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, self.storage.get, file_path
        )

    async def save(self, file_obj: BinaryIO, file_path: str) -> str:
        """Async version of save."""
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: self.storage.save(file_obj, file_path)
        )

    async def delete(self, file_path: str) -> bool:
        """Async version of delete."""
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, self.storage.delete, file_path
        )