import os

import pytest

from app.models import DocumentSummary, DocumentHistory
from app.services.database_service import DatabaseService


class TestDatabaseService:
    def test_init_requires_database_path(self, monkeypatch):
        """Test that DatabaseService requires DATABASE_PATH environment variable"""
        monkeypatch.delenv("DATABASE_PATH", raising=False)

        with pytest.raises(ValueError, match="DATABASE_PATH environment variable is required"):
            DatabaseService()

    def test_init_creates_database(self, temp_db_path, monkeypatch):
        """Test that DatabaseService initializes database correctly"""
        monkeypatch.setenv("DATABASE_PATH", temp_db_path)

        db_service = DatabaseService()
        assert db_service.db_path == temp_db_path
        assert os.path.exists(temp_db_path)

    def test_save_document_summary(self, temp_db_path, monkeypatch):
        """Test saving document summary to database"""
        monkeypatch.setenv("DATABASE_PATH", temp_db_path)
        db_service = DatabaseService()

        document = DocumentSummary(filename="test.pdf", summary="Test summary", file_size=1024, page_count=5)

        result = db_service.save_document_summary(document)
        assert result is True

    def test_get_last_5_documents(self, temp_db_path, monkeypatch):
        """Test retrieving last 5 documents"""
        monkeypatch.setenv("DATABASE_PATH", temp_db_path)
        db_service = DatabaseService()

        # Save test documents
        for i in range(3):
            document = DocumentSummary(
                filename=f"test{i}.pdf", summary=f"Test summary {i}", file_size=1024 + i, page_count=5 + i
            )
            db_service.save_document_summary(document)

        documents = db_service.get_last_5_documents()
        assert len(documents) == 3
        assert all(isinstance(doc, DocumentHistory) for doc in documents)

    def test_get_document_by_id_exists(self, temp_db_path, monkeypatch):
        """Test retrieving existing document by ID"""
        monkeypatch.setenv("DATABASE_PATH", temp_db_path)
        db_service = DatabaseService()

        document = DocumentSummary(filename="test.pdf", summary="Test summary", file_size=1024, page_count=5)
        db_service.save_document_summary(document)

        retrieved = db_service.get_document_by_id(document.id)
        assert retrieved is not None
        assert retrieved.id == document.id
        assert retrieved.filename == document.filename

    def test_get_document_by_id_not_exists(self, temp_db_path, monkeypatch):
        """Test retrieving non-existing document by ID returns None"""
        monkeypatch.setenv("DATABASE_PATH", temp_db_path)
        db_service = DatabaseService()

        retrieved = db_service.get_document_by_id("non-existing-id")
        assert retrieved is None

    def test_database_error_handling(self, monkeypatch):
        """Test database error handling returns appropriate values"""
        monkeypatch.setenv("DATABASE_PATH", "/invalid/path/test.db")

        with pytest.raises(Exception):
            DatabaseService()
