import os
import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

# Set test environment variables
os.environ["DATABASE_PATH"] = tempfile.mktemp(suffix=".db")
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"


@pytest.fixture
def load_pdf_bytes():
    """Fixture to load any PDF file from the fixtures directory by name"""

    def _load_pdf(filename: str) -> bytes:
        pdf_path = Path(__file__).parent / "fixtures" / filename
        if not pdf_path.exists():
            raise FileNotFoundError(f"Test PDF file not found: {pdf_path}")
        return pdf_path.read_bytes()

    return _load_pdf


@pytest.fixture
def sample_pdf_bytes():
    """Fixture that provides sample PDF bytes"""
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n178\n%%EOF"


@pytest.fixture
def invalid_pdf_bytes():
    """Fixture that provides invalid PDF bytes"""
    return b"This is not a PDF file"


@pytest.fixture
def temp_db_path():
    """Fixture that provides a temporary database path"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def mock_openai_client():
    """Fixture that provides a mocked OpenAI client"""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Test summary"
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def test_client():
    """Fixture that provides a FastAPI test client"""
    from app.main import app
    return TestClient(app)
