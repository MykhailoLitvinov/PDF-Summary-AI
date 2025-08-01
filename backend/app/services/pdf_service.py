import base64
import logging
from io import BytesIO
from typing import Tuple, Dict

import pdfplumber

logger = logging.getLogger(__name__)


class PDFService:
    def __init__(self):
        self.MAX_FILE_SIZE = 52428800  # 50MB hardcoded limit
        self.MAX_PAGES = 100  # 100 pages hardcoded limit
        self.MAX_IMAGES = 20  # limit for image extraction

    def validate_pdf(self, file_content: bytes, filename: str) -> Tuple[bool, str]:
        """Validate PDF file"""
        try:
            # Check file size
            if len(file_content) > self.MAX_FILE_SIZE:
                return False, f"The file is too large. Maximum size: {self.MAX_FILE_SIZE // (1024*1024)}MB"

            # Check if it's a PDF file
            if not filename.lower().endswith(".pdf"):
                return False, "Only PDF files are supported"

            # Check PDF file signature
            if not file_content.startswith(b"%PDF-"):
                return False, "Invalid PDF file format"

            # Check if the file is readable
            pdf_stream = BytesIO(file_content)
            with pdfplumber.open(pdf_stream) as pdf:
                page_count = len(pdf.pages)

                if page_count > self.MAX_PAGES:
                    return False, f"Too many pages. Maximum allowed: {self.MAX_PAGES}"

                if page_count == 0:
                    return False, "The PDF file is empty"

            return True, "OK"

        except Exception as e:
            logger.error(f"PDF validation error: {str(e)}")
            return False, "Failed to read PDF file"

    def extract_pdf_content(self, file_content: bytes) -> Dict[str, any]:
        """Extract text from PDF, including tables"""
        try:
            pdf_stream = BytesIO(file_content)
            extracted_data = {"text": "", "tables": [], "images": [], "page_count": 0, "metadata": {}}

            with pdfplumber.open(pdf_stream) as pdf:
                extracted_data["page_count"] = len(pdf.pages)

                # Extract metadata
                if pdf.metadata:
                    extracted_data["metadata"] = {
                        "title": pdf.metadata.get("Title", ""),
                        "author": pdf.metadata.get("Author", ""),
                        "subject": pdf.metadata.get("Subject", ""),
                        "creator": pdf.metadata.get("Creator", ""),
                    }

                all_text = []

                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        all_text.append(f"=== Page {page_num} ===\n{page_text}\n")

                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table_num, table in enumerate(tables, 1):
                            extracted_data["tables"].append({"page": page_num, "table_num": table_num, "data": table})

                            # Append table as text
                            table_text = self._table_to_text(table)
                            all_text.append(f"=== Table {table_num} on page {page_num} ===\n{table_text}\n")

                    # Extract images
                    images = page.images
                    if images and len(extracted_data["images"]) < self.MAX_IMAGES:
                        for img_index, img in enumerate(images, 1):
                            # Crop image region
                            cropped = page.crop((img["x0"], img["top"], img["x1"], img["bottom"]))
                            pil_img = cropped.to_image(resolution=300).original

                            # Convert to base64
                            img_byte_arr = BytesIO()
                            try:
                                pil_img.save(img_byte_arr, format="PNG")
                                img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

                                extracted_data["images"].append(
                                    {"page": page_num, "image_num": img_index, "base64": img_base64}
                                )
                            finally:
                                img_byte_arr.close()
                                pil_img.close()

                extracted_data["text"] = "\n".join(all_text)

            return extracted_data

        except Exception as e:
            logger.error(f"PDF text extraction error: {str(e)}")
            raise Exception(f"Failed to process PDF file: {str(e)}")

    @staticmethod
    def _table_to_text(table) -> str:
        """Convert table to plain text"""
        if not table:
            return ""

        text_rows = []
        for row in table:
            if row:
                # Replace None with empty string and join columns
                clean_row = [str(cell) if cell is not None else "" for cell in row]
                text_rows.append(" | ".join(clean_row))

        return "\n".join(text_rows)
