from unittest.mock import patch, Mock


class TestDocumentEndpoints:
    def test_health_endpoint(self, test_client):
        """Test health endpoint"""
        response = test_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self, test_client):
        """Test root endpoint"""
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "PDF Summary AI Backend"
        assert response.json()["status"] == "running"

    def test_upload_pdf_success(self, test_client, sample_pdf_bytes):
        """Test successful PDF upload"""
        with patch("app.services.pdf_service.PDFService.validate_pdf") as mock_validate, patch(
            "app.services.pdf_service.PDFService.extract_pdf_content"
        ) as mock_extract, patch("app.services.openai_service.OpenAIService.generate_summary") as mock_summary, patch(
            "app.services.database_service.DatabaseService.save_document_summary"
        ) as mock_save:

            mock_validate.return_value = (True, "OK")
            mock_extract.return_value = {"text": "Sample text", "images": [], "page_count": 1}
            mock_summary.return_value = "Test summary"
            mock_save.return_value = True

            files = {"file": ("test.pdf", sample_pdf_bytes, "application/pdf")}
            response = test_client.post("/api/documents/upload", files=files)

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "id" in data["data"]
            assert data["data"]["summary"] == "Test summary"

    def test_upload_pdf_validation_error(self, test_client, sample_pdf_bytes):
        """Test upload with PDF validation error"""
        with patch("app.services.pdf_service.PDFService.validate_pdf") as mock_validate:
            mock_validate.return_value = (False, "File too large")

            files = {"file": ("test.pdf", sample_pdf_bytes, "application/pdf")}
            response = test_client.post("/api/documents/upload", files=files)

            assert response.status_code == 400
            assert response.json()["detail"] == "File too large"

    def test_upload_pdf_extraction_error(self, test_client, sample_pdf_bytes):
        """Test upload with PDF extraction error"""
        with patch("app.services.pdf_service.PDFService.validate_pdf") as mock_validate, patch(
            "app.services.pdf_service.PDFService.extract_pdf_content"
        ) as mock_extract:

            mock_validate.return_value = (True, "OK")
            mock_extract.return_value = {"text": "", "images": [], "page_count": 1}

            files = {"file": ("test.pdf", sample_pdf_bytes, "application/pdf")}
            response = test_client.post("/api/documents/upload", files=files)

            assert response.status_code == 400
            assert "Failed to extract text" in response.json()["detail"]

    def test_upload_pdf_processing_error(self, test_client, sample_pdf_bytes):
        """Test upload with processing error returns generic message"""
        with patch("app.services.pdf_service.PDFService.validate_pdf") as mock_validate:
            mock_validate.side_effect = Exception("Detailed error message")

            files = {"file": ("test.pdf", sample_pdf_bytes, "application/pdf")}
            response = test_client.post("/api/documents/upload", files=files)

            assert response.status_code == 500
            # Should return generic error message, not detailed error
            assert response.json()["detail"] == "Error processing file"

    def test_get_history_success(self, test_client):
        """Test successful history retrieval"""
        with patch("app.services.database_service.DatabaseService.get_last_5_documents") as mock_get:
            mock_doc = Mock()
            mock_doc.id = "test-id"
            mock_doc.filename = "test.pdf"
            mock_doc.summary = "Short summary"
            mock_doc.upload_date.isoformat.return_value = "2023-01-01T00:00:00"
            mock_doc.file_size = 1024
            mock_doc.page_count = 1

            mock_get.return_value = [mock_doc]

            response = test_client.get("/api/documents/history")

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["data"]["documents"]) == 1

    def test_get_history_error(self, test_client):
        """Test history retrieval error returns generic message"""
        with patch("app.services.database_service.DatabaseService.get_last_5_documents") as mock_get:
            mock_get.side_effect = Exception("Database connection failed")

            response = test_client.get("/api/documents/history")

            assert response.status_code == 500
            # Should return generic error message
            assert response.json()["detail"] == "Error retrieving history"

    def test_get_document_success(self, test_client):
        """Test successful single document retrieval"""
        with patch("app.services.database_service.DatabaseService.get_document_by_id") as mock_get:
            mock_doc = Mock()
            mock_doc.id = "test-id"
            mock_doc.filename = "test.pdf"
            mock_doc.summary = "Full summary"
            mock_doc.upload_date.isoformat.return_value = "2023-01-01T00:00:00"
            mock_doc.file_size = 1024
            mock_doc.page_count = 1

            mock_get.return_value = mock_doc

            response = test_client.get("/api/documents/test-id")

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["id"] == "test-id"

    def test_get_document_not_found(self, test_client):
        """Test document not found"""
        with patch("app.services.database_service.DatabaseService.get_document_by_id") as mock_get:
            mock_get.return_value = None

            response = test_client.get("/api/documents/non-existing-id")

            assert response.status_code == 404
            assert response.json()["detail"] == "Document not found"
