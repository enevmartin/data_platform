# apps/core/storage/media_storage.py
import os
import mimetypes
from typing import BinaryIO, Optional, Tuple
from PIL import Image
from io import BytesIO
from .base import StorageInterface


class MediaStorage(StorageInterface):
    """Specialized storage for media files with thumbnail generation."""

    def __init__(self, storage: StorageInterface, thumbnail_sizes: List[Tuple[int, int]] = [(100, 100), (200, 200)]):
        """
        Initialize media storage.

        Args:
            storage: Base storage implementation
            thumbnail_sizes: List of thumbnail sizes to generate
        """
        self.storage = storage
        self.thumbnail_sizes = thumbnail_sizes

    def _get_media_type(self, file_path: str) -> str:
        """Get media type from file path."""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            return 'application/octet-stream'
        return mime_type

    def _is_image(self, file_path: str) -> bool:
        """Check if file is an image."""
        media_type = self._get_media_type(file_path)
        return media_type.startswith('image/')

    def _generate_thumbnail_path(self, file_path: str, size: Tuple[int, int]) -> str:
        """Generate thumbnail path."""
        base_name, ext = os.path.splitext(file_path)
        return f"{base_name}_thumb_{size[0]}x{size[1]}{ext}"

    def _generate_thumbnails(self, image_data: bytes, file_path: str) -> None:
        """Generate thumbnails for an image."""
        try:
            with Image.open(BytesIO(image_data)) as img:
                for size in self.thumbnail_sizes:
                    thumb = img.copy()
                    thumb.thumbnail(size)
                    thumb_io = BytesIO()
                    thumb.save(thumb_io, format=img.format)
                    thumb_io.seek(0)

                    thumb_path = self._generate_thumbnail_path(file_path, size)
                    self.storage.save(thumb_io, thumb_path)
        except Exception as e:
            # Log error but continue
            print(f"Error generating thumbnails: {str(e)}")

    def get(self, file_path: str) -> Optional[BinaryIO]:
        """Get media file."""
        return self.storage.get(file_path)

    def save(self, file_obj: BinaryIO, file_path: str) -> str:
        """Save media file and generate thumbnails if it's an image."""
        # Read the content first
        content = file_obj.read()

        # Save the original file
        result = self.storage.save(BytesIO(content), file_path)

        # Generate thumbnails if it's an image
        if self._is_image(file_path):
            self._generate_thumbnails(content, file_path)

        return result

    def delete(self, file_path: str) -> bool:
        """Delete media file and its thumbnails."""
        # Delete thumbnails
        if self._is_image(file_path):
            for size in self.thumbnail_sizes:
                thumb_path = self._generate_thumbnail_path(file_path, size)
                self.storage.delete(thumb_path)

        # Delete original file
        return self.storage.delete(file_path)