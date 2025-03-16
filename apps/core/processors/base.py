# apps/core/processors/base.py
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    def process(self, datafile):
        """Process the file and update the datafile record"""
        try:
            # Set status to processing
            datafile.status = 'processing'
            datafile.save(update_fields=['status'])

            # Validate file
            validation_result = self.validate(datafile)
            if not validation_result['is_valid']:
                datafile.status = 'failed'
                datafile.save(update_fields=['status'])
                logger.error(f"Validation failed for file {datafile.id}: {validation_result['message']}")
                return False

            # Extract metadata
            metadata = self.extract_metadata(datafile)

            # Process file
            self._process_file(datafile)

            # Update status
            datafile.status = 'processed'
            datafile.save(update_fields=['status'])

            return True
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__} processing file {datafile.id}: {str(e)}")
            datafile.status = 'failed'
            datafile.save(update_fields=['status'])
            return False

    @abstractmethod
    def _process_file(self, datafile):
        """Implement file processing logic"""
        pass

    @abstractmethod
    def validate(self, datafile):
        """Validate the file"""
        pass

    @abstractmethod
    def extract_metadata(self, datafile):
        """Extract metadata from the file"""
        pass