import io
import pytest
from app import app, db, process_file, upload_file
from models import Document  # Ensure this is correctly imported
import tempfile
import os


@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()  # This will automatically use the app context
        db.session.remove()
        db.drop_all()
@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test-api-key')

def test_process_file_pdf(client):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(b'Fake PDF content')
        tmp.seek(0)  # Rewind the file before reading it in the test function
        response = process_file(tmp.name, 'tempfile.pdf', 1)

    assert response[1] == 200
    assert 'uploaded successfully' in response[0].json['message']



def test_upload_file(client):
    data = {
        'file': (io.BytesIO(b"Fake file content"), 'test.pdf'),
        'userId': '1'
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # Verify
    assert response.status_code == 202
    assert 'Files queued for processing' in response.json['message']

@pytest.mark.parametrize("file_extension, content_type", [
    ('.pdf', 'application/pdf'),
    ('.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
])
def test_process_file_various_formats(client, file_extension, content_type):
    with tempfile.NamedTemporaryFile(suffix=file_extension) as tmp:
        tmp.write(b'Fake content based on file type')
        tmp.seek(0)
        filename = f'tempfile{file_extension}'
        response = process_file(tmp.name, filename, 1)

    assert response[1] == 200
    assert 'uploaded successfully' in response[0].json['message']
def test_upload_file_no_user_id(client):
    data = {
        'file': (io.BytesIO(b"Fake file content"), 'test.pdf')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # Verify
    assert response.status_code == 400
    assert 'UserId is required' in response.json['error']

def test_upload_file_unsupported_type(client):
    data = {
        'file': (io.BytesIO(b"Fake file content"), 'test.xyz'),
        'userId': '1'
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # Verify
    assert response.status_code == 400
    assert 'File type not allowed' in response.json['error']

def test_file_access_with_user_session(client):
    # Assume you have session management
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Simulate a logged-in user

    response = client.get('/api/documents/user/1')
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()
