from backend.app.services.pdf_service import PDFService


def test_validate_pdf_success(load_pdf_bytes):
    service = PDFService()
    filename = "dummy.pdf"
    is_valid, message = service.validate_pdf(load_pdf_bytes(filename), filename)
    assert is_valid is True
    assert message == "OK"


def test_extract_text_with_tables(load_pdf_bytes):
    filename = "dummy.pdf"
    pdf_bytes = load_pdf_bytes(filename)
    service = PDFService()

    result = service.extract_text_with_tables(pdf_bytes)

    assert "text" in result
    assert "tables" in result
    assert "page_count" in result
    assert "metadata" in result

    assert result["page_count"] > 0
    assert "Dummy PDF file" in result["text"]
