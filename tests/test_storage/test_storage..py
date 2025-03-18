# tests/test_storage.py
import unittest
import tempfile
import os
from io import BytesIO
from apps.core.storage.local import LocalStorage


class TestLocalStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = LocalStorage(base_dir=self.temp_dir)
        self.test_content = b"Test content"
        self.test_file = BytesIO(self.test_content)

    def tearDown(self):
        # Clean up temp files
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_save_and_get(self):
        # Test saving and retrieving a file
        file_path = "test_file.txt"
        saved_path = self.storage.save(self.test_file, file_path)
        self.assertEqual(saved_path, file_path)

        retrieved_file = self.storage.get(file_path)
        self.assertIsNotNone(retrieved_file)
        self.assertEqual(retrieved_file.read(), self.test_content)

    def test_delete(self):
        # Test deleting a file
        file_path = "test_delete.txt"
        self.storage.save(self.test_file, file_path)

        # File should exist
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, file_path)))

        # Delete and verify
        result = self.storage.delete(file_path)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, file_path)))