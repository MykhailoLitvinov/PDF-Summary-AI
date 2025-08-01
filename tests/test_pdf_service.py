from unittest.mock import patch, Mock

from app.services.pdf_service import PDFService


class TestPDFService:
    def test_init_with_hardcoded_limits(self):
        """Test PDFService initialization with hardcoded limits"""
        service = PDFService()
        assert service.MAX_FILE_SIZE == 52428800  # 50MB
        assert service.MAX_PAGES == 100

    def test_validate_pdf_valid_file(self, sample_pdf_bytes):
        """Test PDF validation with valid PDF file"""
        service = PDFService()

        with patch("pdfplumber.open") as mock_open:
            mock_pdf = Mock()
            mock_pdf.pages = [Mock()]  # 1 page
            mock_open.return_value.__enter__.return_value = mock_pdf

            is_valid, message = service.validate_pdf(sample_pdf_bytes, "test.pdf")
            assert is_valid is True
            assert message == "OK"

    def test_validate_pdf_too_large(self, sample_pdf_bytes):
        """Test PDF validation with file too large"""
        service = PDFService()
        service.MAX_FILE_SIZE = 10  # Very small limit

        is_valid, message = service.validate_pdf(sample_pdf_bytes, "test.pdf")
        assert is_valid is False
        assert "too large" in message

    def test_validate_pdf_invalid_extension(self, sample_pdf_bytes):
        """Test PDF validation with invalid file extension"""
        service = PDFService()

        is_valid, message = service.validate_pdf(sample_pdf_bytes, "test.txt")
        assert is_valid is False
        assert "Only PDF files are supported" in message

    def test_validate_pdf_invalid_signature(self, invalid_pdf_bytes):
        """Test PDF validation with invalid PDF signature"""
        service = PDFService()

        is_valid, message = service.validate_pdf(invalid_pdf_bytes, "test.pdf")
        assert is_valid is False
        assert "Invalid PDF file format" in message

    def test_validate_pdf_too_many_pages(self, sample_pdf_bytes):
        """Test PDF validation with too many pages"""
        service = PDFService()
        service.MAX_PAGES = 1

        with patch("pdfplumber.open") as mock_open:
            mock_pdf = Mock()
            mock_pdf.pages = [Mock(), Mock()]  # 2 pages
            mock_open.return_value.__enter__.return_value = mock_pdf

            is_valid, message = service.validate_pdf(sample_pdf_bytes, "test.pdf")
            assert is_valid is False
            assert "Too many pages" in message

    def test_validate_pdf_empty_file(self, sample_pdf_bytes):
        """Test PDF validation with empty PDF file"""
        service = PDFService()

        with patch("pdfplumber.open") as mock_open:
            mock_pdf = Mock()
            mock_pdf.pages = []  # 0 pages
            mock_open.return_value.__enter__.return_value = mock_pdf

            is_valid, message = service.validate_pdf(sample_pdf_bytes, "test.pdf")
            assert is_valid is False
            assert "empty" in message

    def test_validate_pdf_corrupted_file(self, sample_pdf_bytes):
        """Test PDF validation with corrupted PDF file"""
        service = PDFService()

        with patch("pdfplumber.open") as mock_open:
            mock_open.side_effect = Exception("Corrupted PDF")

            is_valid, message = service.validate_pdf(sample_pdf_bytes, "test.pdf")
            assert is_valid is False
            assert "Failed to read PDF file" in message

    def test_extract_pdf_content_success(self, sample_pdf_bytes):
        """Test successful PDF content extraction"""
        service = PDFService()

        with patch("pdfplumber.open") as mock_open:
            mock_page = Mock()
            mock_page.extract_text.return_value = "Sample text"
            mock_page.extract_tables.return_value = []
            mock_page.images = []

            mock_pdf = Mock()
            mock_pdf.pages = [mock_page]
            mock_pdf.metadata = {"Title": "Test PDF"}
            mock_open.return_value.__enter__.return_value = mock_pdf

            result = service.extract_pdf_content(sample_pdf_bytes)

            assert "text" in result
            assert "Sample text" in result["text"]
            assert result["page_count"] == 1
            assert result["metadata"]["title"] == "Test PDF"

    def test_table_to_text_empty(self):
        """Test table to text conversion with empty table"""
        result = PDFService._table_to_text(None)
        assert result == ""

        result = PDFService._table_to_text([])
        assert result == ""

    def test_table_to_text_with_data(self):
        """Test table to text conversion with data"""
        table = [["Header1", "Header2"], ["Value1", "Value2"], [None, "Value3"]]

        result = PDFService._table_to_text(table)
        lines = result.split("\n")

        assert "Header1 | Header2" in lines[0]
        assert "Value1 | Value2" in lines[1]
        assert " | Value3" in lines[2]


# Integration tests with real PDF files
def test_validate_pdf_success_real_file(load_pdf_bytes):
    """Integration test with real PDF file"""
    service = PDFService()
    filename = "dummy.pdf"
    is_valid, message = service.validate_pdf(load_pdf_bytes(filename), filename)
    assert is_valid is True
    assert message == "OK"


def test_extract_text_dummy_real_file(load_pdf_bytes):
    """Integration test with real dummy PDF"""
    filename = "dummy.pdf"
    pdf_bytes = load_pdf_bytes(filename)
    service = PDFService()

    result = service.extract_pdf_content(pdf_bytes)

    assert "text" in result
    assert "tables" in result
    assert "page_count" in result
    assert "metadata" in result
    assert result["page_count"] > 0


def test_extract_content_real_file(load_pdf_bytes):
    """Integration test with real dummy PDF"""
    filename = "sample.pdf"
    pdf_bytes = load_pdf_bytes(filename)
    service = PDFService()

    result = service.extract_pdf_content(pdf_bytes)

    assert "tables" in result
    assert "images" in result

    assert len(result["tables"]) > 0
    assert len(result["images"]) > 0

    assert "base64" in result["images"][0]
