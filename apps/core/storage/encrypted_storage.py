# apps/core/storage/encrypted_storage.py
import os
from cryptography.fernet import Fernet
from typing import BinaryIO, Optional
from io import BytesIO
from .base import StorageInterface


class EncryptedStorage(StorageInterface):
    """Storage decorator that adds encryption."""

    def __init__(self, storage: StorageInterface, key: Optional[str] = None):
        """
        Initialize encrypted storage.

        Args:
            storage: Base storage implementation
            key: Encryption key (will be generated if None)
        """
        self.storage = storage

        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key.encode() if isinstance(key, str) else key

        self.cipher = Fernet(self.key)

    def get(self, file_path: str) -> Optional[BinaryIO]:
        """Get and decrypt file."""
        encrypted_data = self.storage.get(file_path)
        if encrypted_data is None:
            return None

        # Decrypt data
        encrypted_content = encrypted_data.read()
        try:
            decrypted_content = self.cipher.decrypt(encrypted_content)
            return BytesIO(decrypted_content)
        except:
            # If decryption fails, return None
            return None

    def save(self, file_obj: BinaryIO, file_path: str) -> str:
        """Encrypt and save file."""
        content = file_obj.read()
        encrypted_content = self.cipher.encrypt(content)

        return self.storage.save(BytesIO(encrypted_content), file_path)

    def delete(self, file_path: str) -> bool:
        """Delete encrypted file."""
        return self.storage.delete(file_path)