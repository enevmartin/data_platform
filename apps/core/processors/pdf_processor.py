import logging
import PyPDF2
import os
from typing import Dict, Any, Optional

from .base import BaseProcessor

logger = logging.getLogger(__name__)


class PDFProcessor(BaseProcessor):
    """Processor for PDF files."""

    def _process_file(self, datafile) -> None:
        """Process a PDF file."""
        file_path = datafile.file.path
        logger.info(f"Processing PDF file: {file_path}")

        try:
            # Extract text from PDF
            text_content = self._extract_text(file_path)

            # Save extracted text to a new file
            text_path = f"{os.path.splitext(file_path)[0]}.txt"
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text_content)

            # Update datafile with text path
            datafile.processed_file = text_path
            datafile.save(update_fields=['processed_file'])

        except Exception as e:
            logger.exception(f"Error processing PDF file {file_path}")
            raise

    def _extract_text(self, file_path: str) -> str:
        """Extract text content from a PDF file."""
        text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text.append(page.extract_text())
        return "\n".join(text)

    def validate(self, datafile) -> Dict[str, Any]:
        """Validate that the file is a valid PDF."""
        try:
            # Check file extension
            if not datafile.file.name.lower().endswith('.pdf'):
                return {'is_valid': False, 'message': 'File is not a PDF'}

            # Try to open with PyPDF2
            with open(datafile.file.path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # Check if PDF has pages
                if len(pdf_reader.pages) == 0:
                    return {'is_valid': False, 'message': 'PDF has no pages'}

            return {'is_valid': True, 'message': 'Valid PDF file'}
        except Exception as e:
            return {'is_valid': False, 'message': f'Invalid PDF file: {str(e)}'}

    def extract_metadata(self, datafile) -> Optional[Dict[str, Any]]:
        """Extract metadata from the PDF file."""
        try:
            metadata = {}
            with open(datafile.file.path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                metadata['page_count'] = len(pdf.pages)

                # Extract document info if available
                if pdf.metadata:
                    pdf_info = pdf.metadata
                    for key in pdf_info:
                        if key.startswith('/'):
                            clean_key = key[1:].lower()
                            metadata[clean_key] = str(pdf_info[key])

                # Extract first page text as sample
                if len(pdf.pages) > 0:
                    sample_text = pdf.pages[0].extract_text()
                    # Limit sample text to first 500 characters
                    metadata['sample_text'] = sample_text[:500] + ('...' if len(sample_text) > 500 else '')

            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata from PDF: {str(e)}")
            return None