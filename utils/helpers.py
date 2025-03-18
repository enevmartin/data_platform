class StorageHealthCheck:
    def check_health(self) -> Dict[str, Any]:
        test_content = b"test_content"
        test_path = "health_check_test.txt"

        try:
            # Combined write/read operations
            self.storage.save(test_content, test_path)
            retrieved = self.storage.get(test_path)
            read_content = retrieved.read() if retrieved else None

            # Clean up regardless of outcome
            try:
                self.storage.delete(test_path)
            except Exception:
                pass  # Silently fail cleanup

            # Return based on content match
            content_match = test_content == read_content
            status = "healthy" if content_match else "degraded"
            message = "Storage is working correctly" if content_match else "Storage read/write mismatch"

            return {
                'status': status,
                'message': message,
                'details': {
                    'write_success': True,
                    'read_success': retrieved is not None,
                    'content_match': content_match
                }
            }

        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Storage health check failed: {str(e)}',
                'details': {
                    'error': str(e),
                    'error_type': type(e).__name__
                }
            }