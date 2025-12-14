"""
Basic tests for the TranslationService functionality.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from uuid import UUID
import os

from ..services.translation_service import TranslationService
from ..models.translation import Translation


class TestTranslationService:
    """Test class for TranslationService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.translation_service = TranslationService()
        self.mock_db = Mock(spec=Session)
        self.chapter_id = UUID('12345678-1234-5678-1234-567812345678')

    def test_translate_preserving_structure_with_code_blocks(self):
        """Test that code blocks are preserved during translation."""
        original_content = """
# Introduction to Robotics

This is a sample text with `inline code` and a code block:

```
def hello_world():
    print("Hello, World!")
```

The code should remain unchanged after translation.
"""

        # Mock the translation response to simulate translation
        with patch.object(self.translation_service, 'translate_chapter_content') as mock_translate:
            mock_translate.return_value = """
# روبوٹکس کا تعارف

یہ ایک نمونہ متن ہے جس میں `inline code` اور ایک کوڈ بلاک ہے:

```
def hello_world():
    print("Hello, World!")
```

کوڈ کو ترجمہ کے بعد بے تبدیل رہنا چاہیے۔
"""
            result = self.translation_service.translate_preserving_structure(
                original_content,
                "Urdu"
            )

            # Check that code blocks are preserved
            assert "def hello_world():" in result
            assert 'print("Hello, World!")' in result
            assert "`inline code`" in result  # Inline code should be preserved

    def test_translate_preserving_structure_with_headings(self):
        """Test that headings are preserved during translation."""
        original_content = """
# Main Heading
## Sub Heading
This is content under headings.
### Another Heading
More content here.
"""

        expected_result = """
# Main Heading
## Sub Heading
This is translated content under headings.
### Another Heading
More translated content here.
"""

        with patch.object(self.translation_service, 'translate_chapter_content') as mock_translate:
            mock_translate.return_value = expected_result
            result = self.translation_service.translate_preserving_structure(
                original_content,
                "Urdu"
            )

            # Check that headings are preserved
            assert "# Main Heading" in result
            assert "## Sub Heading" in result
            assert "### Another Heading" in result

    def test_translate_text_chunk(self):
        """Test basic text chunk translation."""
        text_chunk = "Hello, this is a test."
        result = self.translation_service.translate_text_chunk(text_chunk, "Urdu")

        # Should return the original text if translation fails (which it will in testing without API)
        assert result == text_chunk

    def test_translate_chatbot_response(self):
        """Test chatbot response translation."""
        response = "This is a helpful response."
        result = self.translation_service.translate_chatbot_response(response, "Urdu")

        # Should return the original response if translation fails
        assert result == response

    def test_create_and_get_cached_translation(self):
        """Test creating and retrieving cached translations."""
        content = "Test content for translation"

        # Mock the database operations
        mock_translation = Mock(spec=Translation)
        mock_translation.urdu_content = "Translated content"
        mock_translation.expires_at = MagicMock()
        mock_translation.expires_at.__gt__ = lambda x: True  # Always return True for active

        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = mock_translation

        # Test getting cached translation
        cached = self.translation_service.get_cached_translation(
            self.mock_db,
            self.chapter_id
        )

        assert cached is not None
        assert cached.urdu_content == "Translated content"

    def test_translation_quality_validation(self):
        """Test translation quality validation."""
        original = "This is a test sentence with some content."
        good_translation = "This is a translated version of the original content."
        poor_translation = "Short."  # Less than 50% of original length

        # Good translation should have high quality score
        quality_good = self.translation_service.validate_translation_quality(
            original,
            good_translation
        )
        assert quality_good > 0.5

        # Poor translation (too short) should have low quality score
        quality_poor = self.translation_service.validate_translation_quality(
            original,
            poor_translation
        )
        assert quality_poor == 0.0


if __name__ == "__main__":
    pytest.main([__file__])