# apps/core/processors/base.py
from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    """Base class for all file processors."""

    def process(self, datafile) -> bool:
        """
        Process the file and update the datafile record.

        Args:
            datafile: The datafile object to process

        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            # Set status to processing
            self._update_status(datafile, 'processing')

            # Validate file
            validation_result = self.validate(datafile)
            if not validation_result['is_valid']:
                self._update_status(datafile, 'failed')
                logger.error(f"Validation failed for file {datafile.id}: {validation_result['message']}")
                return False

            # Extract metadata
            metadata = self.extract_metadata(datafile)
            if metadata:
                self._update_metadata(datafile, metadata)

            # Process file
            self._process_file(datafile)

            # Update status
            self._update_status(datafile, 'processed')
            return True

        except Exception as e:
            logger.exception(f"Error in {self.__class__.__name__} processing file {datafile.id}")
            self._update_status(datafile, 'failed')
            return False

    def _update_status(self, datafile, status: str) -> None:
        """Update the status of the datafile."""
        datafile.status = status
        datafile.save(update_fields=['status'])

    def _update_metadata(self, datafile, metadata: Dict[str, Any]) -> None:
        """Update the metadata of the datafile."""
        datafile.metadata = metadata
        datafile.save(update_fields=['metadata'])

    @abstractmethod
    def _process_file(self, datafile) -> None:
        """Implement file processing logic."""
        pass

    @abstractmethod
    def validate(self, datafile) -> Dict[str, Any]:
        """
        Validate the file.

        Returns:
            Dict containing at least {'is_valid': bool, 'message': str}
        """
        pass

    @abstractmethod
    def extract_metadata(self, datafile) -> Optional[Dict[str, Any]]:
        """
        Extract metadata from the file.

        Returns:
            Dict of metadata or None if extraction failed
        """
        pass