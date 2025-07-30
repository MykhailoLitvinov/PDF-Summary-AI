import pytest
from pathlib import Path


@pytest.fixture
def load_pdf_bytes():
    """Fixture to load any PDF file from the fixtures directory by name"""

    def _load_pdf(filename: str) -> bytes:
        pdf_path = Path(__file__).parent / "fixtures" / filename
        if not pdf_path.exists():
            raise FileNotFoundError(f"Test PDF file not found: {pdf_path}")
        return pdf_path.read_bytes()

    return _load_pdf
