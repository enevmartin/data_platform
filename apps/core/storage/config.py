# apps/core/storage/config.py
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class StorageConfig:
    """Configuration for storage backends."""
    storage_type: str
    settings: Dict[str, Any]

    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'StorageConfig':
        return cls(
            storage_type=config_dict.get('type', 'local'),
            settings=config_dict.get('settings', {})
        )