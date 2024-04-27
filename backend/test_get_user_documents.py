import pytest
from app import app
from models import Document
from flask import json
from pytest_mock import MockerFixture

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestGetUserDocuments:

    def test_returns_list_of_documents(self, client, mocker):
        mocker.patch('models.Document.query.filter_by', return_value=[Document(), Document()])
        response = client.get('/api/documents/user/user_id')
        assert isinstance(response.json, list)

    def test_returns_200_status_code(self, client, mocker):
        mocker.patch('models.Document.query.filter_by', return_value=[Document(), Document()])
        response = client.get('/api/documents/user/user_id')
        assert response.status_code == 200

    def test_returns_empty_list_if_no_documents_found(self, client, mocker):
        mocker.patch('models.Document.query.filter_by', return_value=[])
        response = client.get('/api/documents/user/user_id')
        assert response.json == []
