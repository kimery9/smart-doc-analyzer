

from app import app, extract_text_from_pdf

# Dependencies:
# pip install pytest-mock
import pytest
import fitz

class TestExtractTextFromPdf:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker, monkeypatch):
        self.mock_doc = mocker.MagicMock()
        self.mocker = mocker
        mocker.patch('fitz.open', return_value=self.mock_doc)
        monkeypatch.setenv('OPENAI_API_KEY', 'fake-api-key')
        # Simple test to check text extraction from a single-page PDF

    def test_simple_text_extraction(self, mocker):
        # Setup a single mock page
        mock_page = mocker.MagicMock()
        mock_page.get_text.return_value = "Simple text extraction"
        mock_doc = mocker.MagicMock()
        mock_doc.__iter__.return_value = [mock_page]
        mocker.patch("fitz.open", return_value=mock_doc)  # Make sure this path matches the actual import

        # Call the function under test
        result = extract_text_from_pdf("single_page.pdf")

        # Assert the result matches the expected text
        assert result == "Simple text extraction"

    #  Returns an empty string if the PDF file is empty.
    def test_extract_text_from_pdf_empty_file(self, mocker):
        # Mock the fitz.open method to return a document with no pages
        mock_doc = mocker.MagicMock()
        mock_doc.__iter__.return_value = []
        mocker.patch("fitz.open", return_value=mock_doc)

        # Call the function under test
        result = extract_text_from_pdf("test.pdf")

        # Assert the result is an empty string
        assert result == ""

    #  Raises an exception if the PDF file is not found or cannot be opened.
    def test_extract_text_from_pdf_file_not_found(self, mocker):
        # Mock the fitz.open method to raise an exception indicating file not found or cannot be opened
        mocker.patch("fitz.open", side_effect=FileNotFoundError("File not found"))

        # Call the function under test
        result = extract_text_from_pdf("nonexistent.pdf")

        # Check that the function handled the exception and returned an empty string
        assert result == "", "Expected empty string on file not found error"
