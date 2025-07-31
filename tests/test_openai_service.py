from unittest.mock import patch

import pytest

from app.services.openai_service import OpenAIService


class TestOpenAIService:
    def test_init_with_api_key(self):
        """Test OpenAIService initialization with API key"""
        service = OpenAIService(api_key="test-key")
        assert service.api_key == "test-key"

    def test_init_with_env_var(self, monkeypatch):
        """Test OpenAIService initialization with environment variable"""
        monkeypatch.setenv("OPENAI_API_KEY", "env-test-key")
        service = OpenAIService()
        assert service.api_key == "env-test-key"

    def test_init_without_api_key(self, monkeypatch):
        """Test OpenAIService initialization without API key raises error"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(ValueError, match="OpenAI API key not found"):
            OpenAIService()

    def test_generate_summary_success(self, mock_openai_client):
        """Test successful summary generation"""
        service = OpenAIService(api_key="test-key")
        service.client = mock_openai_client

        result = service.generate_summary("Test document text", [])

        assert result == "Test summary"
        mock_openai_client.chat.completions.create.assert_called_once()

    def test_generate_summary_with_images(self, mock_openai_client):
        """Test summary generation with images"""
        service = OpenAIService(api_key="test-key")
        service.client = mock_openai_client

        images = [{"image_num": 1, "page": 1, "base64": "test_base64_data"}]
        result = service.generate_summary("Test document text", images)

        assert result == "Test summary"

        # Verify the call was made with correct parameters
        call_args = mock_openai_client.chat.completions.create.call_args
        messages = call_args[1]["messages"]

        # Should have developer prompt, text, and image message
        assert len(messages) == 3
        assert messages[0]["role"] == "developer"
        assert messages[1]["role"] == "user"
        assert "Test document text" in messages[1]["content"]
        assert messages[2]["role"] == "user"

    def test_generate_summary_unexpected_error(self):
        """Test unexpected error handling"""
        service = OpenAIService(api_key="test-key")

        with patch.object(service.client.chat.completions, "create") as mock_create:
            mock_create.side_effect = Exception("Unexpected error")

            with pytest.raises(Exception, match="Summary generation error"):
                service.generate_summary("Test text", [])

    def test_generate_summary_parameters(self, mock_openai_client):
        """Test that generate_summary uses correct parameters"""
        service = OpenAIService(api_key="test-key")
        service.client = mock_openai_client

        service.generate_summary("Test text", [])

        call_args = mock_openai_client.chat.completions.create.call_args
        assert call_args[1]["model"] == "gpt-4o"
        assert call_args[1]["max_tokens"] == 500
        assert call_args[1]["temperature"] == 0.3
