from backend.app.services.pdf_service import PDFService


def test_validate_pdf_success(load_pdf_bytes):
    service = PDFService()
    filename = "dummy.pdf"
    is_valid, message = service.validate_pdf(load_pdf_bytes(filename), filename)
    assert is_valid is True
    assert message == "OK"


def test_extract_text_dummy(load_pdf_bytes):
    filename = "dummy.pdf"
    pdf_bytes = load_pdf_bytes(filename)
    service = PDFService()

    result = service.extract_pdf_content(pdf_bytes)

    assert "text" in result
    assert "tables" in result
    assert "page_count" in result
    assert "metadata" in result

    assert result["page_count"] > 0
    assert "Dummy PDF file" in result["text"]


def test_extract_text_image_table(load_pdf_bytes):
    filename = "sample.pdf"
    pdf_bytes = load_pdf_bytes(filename)
    service = PDFService()

    result = service.extract_pdf_content(pdf_bytes)

    assert len(result["tables"]) > 0
    assert "data" in result["tables"][0]
    assert isinstance(result["tables"][0]["data"], list)

    assert len(result["images"]) > 0
    assert "base64" in result["images"][0]
