# apps/core/storage/health.py
from io import BytesIO
from typing import Dict, Any
from .base import StorageInterface


class StorageHealthCheck:
    """Health check for storage backends."""

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def check_health(self) -> Dict[str, Any]:
        """
        Check if storage is healthy.

        Returns:
            Dict with health status
        """
        try:
            # Create a test file
            test_content = b"Storage health check"
            test_path = ".health_check"

            # Try to save
            self.storage.save(BytesIO(test_content), test_path)

            # Try to get
            retrieved = self.storage.get(test_path)
            read_content = retrieved.read() if retrieved else None

            # Clean up
            self.storage.delete(test_path)

            # Check if content matches
            content_match = test_content == read_content

            return {
                'status': 'healthy' if content_match else 'degraded',
                'message': 'Storage is working correctly' if content_match else 'Storage read/write mismatch',
                'details': {
                    'write_success': True,
                    'read_success': retrieved is not None,
                    'content_match': content_match,
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Storage health check failed: {str(e)}',
                'details': {
                    'error': str(e),
                    'error_type': type(e).__name__,
                }
            }