from tkinter import Image

import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
import pytesseract  # Ensure pytesseract is imported

from app import extract_text_from_image  # Make sure your function is correctly imported


class TestExtractTextFromImage:

    @pytest.fixture(autouse=True)
    def setup_mocks(self, mocker):
        # Patch Image.open globally for all methods
        self.mock_open = mocker.patch('PIL.Image.open', return_value=MagicMock(spec=Image))
        # Patch pytesseract.image_to_string globally for all methods
        self.mock_ocr = mocker.patch('pytesseract.image_to_string', return_value='Text from image')

    def test_returns_text_from_image(self):
        # Call the function under test
        result = extract_text_from_image('image.jpg')

        # Assert the result
        assert result == 'Text from image'

        # Assert that the Image.open() function was called with the correct filepath
        self.mock_open.assert_called_once_with('image.jpg')

        # Assert that the pytesseract.image_to_string() function was called with the correct image
        self.mock_ocr.assert_called_once_with(self.mock_open.return_value)

    #  Handles common image file formats such as PNG, JPG, JPEG, and GIF
    def test_handles_common_image_formats(self):
        # Define file formats to test
        formats = ['image.png', 'image.jpg', 'image.jpeg', 'image.gif']
        for file in formats:
            # Reset mock call counters
            self.mock_open.reset_mock()
            # Call the function under test
            extract_text_from_image(file)
            # Assert that Image.open was called correctly
            self.mock_open.assert_called_once_with(file)

    #  Uses pytesseract library to perform OCR on the image
    def test_uses_pytesseract_library(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Text from image')

        # Call the function under test
        extract_text_from_image('image.jpg')

        # Assert that the pytesseract.image_to_string() function was called with the correct image
        pytesseract.image_to_string.assert_called_once_with(Image.open.return_value)

    #  Handles images with clear and readable text
    def test_handles_clear_and_readable_text(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Text from image')
    
        # Call the function under test
        result = extract_text_from_image('image.jpg')
    
        # Assert the result
        assert result == 'Text from image'

    #  Handles images with multiple lines of text
    def test_handles_multiple_lines_of_text(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Line 1\nLine 2\nLine 3')
    
        # Call the function under test
        result = extract_text_from_image('image.jpg')
    
        # Assert the result
        assert result == 'Line 1\nLine 2\nLine 3'

    #  Handles images with low resolution or poor image quality
    def test_handles_low_resolution_or_poor_quality(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Text from image')
    
        # Call the function under test
        result = extract_text_from_image('image.jpg')
    
        # Assert the result
        assert result == 'Text from image'

    #  Handles images with distorted or skewed text
    def test_handles_distorted_or_skewed_text(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Text from image')
    
        # Call the function under test
        result = extract_text_from_image('image.jpg')
    
        # Assert the result
        assert result == 'Text from image'

    #  Handles images with non-English text
    def test_handles_non_english_text(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Text from image')
    
        # Call the function under test
        result = extract_text_from_image('image.jpg')
    
        # Assert the result
        assert result == 'Text from image'

    #  Handles images with handwritten text
    def test_handles_handwritten_text(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Text from image')
    
        # Call the function under test
        result = extract_text_from_image('image.jpg')
    
        # Assert the result
        assert result == 'Text from image'

    #  Handles images with text overlaying graphics or other elements
    def test_handles_text_overlaying_graphics(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function
        mocker.patch('pytesseract.image_to_string', return_value='Text from image')
    
        # Call the function under test
        result = extract_text_from_image('image.jpg')
    
        # Assert the result
        assert result == 'Text from image'

    #  Raises appropriate exceptions if pytesseract library is not installed or image file is not supported
    def test_raises_exceptions_if_dependencies_not_installed_or_file_not_supported(self, mocker):
        # Mock the Image.open() function
        mocker.patch('PIL.Image.open')
        # Mock the pytesseract.image_to_string() function to raise an exception
        mocker.patch('pytesseract.image_to_string', side_effect=Exception)
    
        # Call the function under test
        with pytest.raises(Exception):
            extract_text_from_image('image.jpg')
