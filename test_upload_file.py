import os
import io
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pytest
from app import app

from app import upload_file

from app import app

# Utility function to create an in-memory file
def create_test_file(filename, content='Default content'):
    # Use BytesIO to simulate a file in memory with given content
    file_stream = io.BytesIO(content.encode('utf-8'))
    # Flask testing uploads require a tuple with filename and file object
    file_tuple = (file_stream, filename)
    return file_tuple
class TestUploadFile:

    def test_upload_file_allowed_extension_success(self):
        # Arrange
        app.config['UPLOAD_FOLDER'] = 'uploads/'
        filename = 'test.txt'
        content = "This is test file content."
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the directory exists and the file does not exist before the test
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        if os.path.exists(file_path):
            os.remove(file_path)

        file = create_test_file(filename, content)
        data = {
            'file': (io.BytesIO(content.encode('utf-8')), filename)
        }

        # Act
        response = app.test_client().post('/upload', data=data, content_type='multipart/form-data')

        # Assert
        assert response.status_code == 200, response.json

        # Cleanup: Remove the uploaded file after the assertion
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_upload_file_invalid_extension_error(self):
        # Arrange
        app.config['UPLOAD_FOLDER'] = 'uploads/'
        filename = 'invalid.exe'
        content = "This should fail."
        data = {'file': create_test_file(filename, content)}

        # Act
        response = app.test_client().post('/upload', data=data, content_type='multipart/form-data')

        # Assert
        assert response.status_code == 400
        assert 'File type not allowed' in response.json['error']

    def test_upload_file_size_exceeds_limit(self):
        # Arrange
        app.config['UPLOAD_FOLDER'] = 'uploads/'
        filename = 'too_large.txt'
        content = "a" * (app.config['MAX_CONTENT_LENGTH'] + 1)  # Create content larger than the max size
        data = {'file': create_test_file(filename, content)}

        # Act
        response = app.test_client().post('/upload', data=data, content_type='multipart/form-data')

        # Assert
        assert response.status_code == 413  # Check if the status code for payload too large is returned

    def test_upload_no_file_part(self):
        # Act
        response = app.test_client().post('/upload', data={}, content_type='multipart/form-data')

        # Assert
        assert response.status_code == 400
        assert 'No file part' in response.json['error']

    def test_upload_empty_filename_error(self):
        # Arrange
        app.config['UPLOAD_FOLDER'] = 'uploads/'
        filename = ''
        content = "Filename is empty."
        data = {'file': create_test_file(filename, content)}

        # Act
        response = app.test_client().post('/upload', data=data, content_type='multipart/form-data')

        # Assert
        assert response.status_code == 400
        assert 'No selected file' in response.json['error']

    def test_upload_file_directory_traversal_attempt(self):
        # Arrange
        app.config['UPLOAD_FOLDER'] = 'uploads/'
        filename = '../test.txt'
        content = "Directory traversal attempt."
        data = {'file': create_test_file(filename, content)}

        # Act
        response = app.test_client().post('/upload', data=data, content_type='multipart/form-data')

        # Assert
        assert response.status_code == 400
        assert 'File type not allowed' in response.json['error']  # Assuming your app blocks such filenames


