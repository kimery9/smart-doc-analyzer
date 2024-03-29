# test_app.py
import io
import unittest
from unittest.mock import patch
from app import app, db  # Importing directly from your app.py

class UploaderBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self.user_id = "user_123"

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('app.file_processing_queue.put')
    def test_successful_upload(self, mock_file_processing_queue_put):
        data = {
            'userId': self.user_id,
            'file': (io.BytesIO(b'This is a test file'), 'test.txt'),
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        mock_file_processing_queue_put.assert_called_once()  # Assuming the file is put into the queue for processing
        self.assertEqual(response.status_code, 202)
        self.assertIn('Files queued for processing: test.txt', response.json['message'])

    def test_upload_no_files_provided(self):
        data = {'userId': self.user_id}
        response = self.client.post('/upload', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('No files selected', response.json['error'])


    @patch('app.file_processing_queue.put')
    def test_empty_filename_skipped(self, mock_file_processing_queue_put):
        data = {
            'userId': self.user_id,
            'file': (io.BytesIO(b''), ''),  # Empty filename
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        mock_file_processing_queue_put.assert_not_called()
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
