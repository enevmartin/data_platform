# apps/core/storage/base.py
class StorageInterface:
    def save(self, file_obj, file_path):
        raise NotImplementedError

    def get(self, file_path):
        raise NotImplementedError

    def delete(self, file_path):
        raise NotImplementedError


# apps/core/storage/local.py
from apps.core.storage.base import StorageInterface
import os


class LocalStorage(StorageInterface):
    def save(self, file_obj, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return file_path