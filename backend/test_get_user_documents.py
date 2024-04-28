# test_get_user_documents.py
import pytest
from flask import Flask
from models import db, Document
from app import app as flask_app  # Assuming 'app' is your Flask app instance

@pytest.fixture(scope='module')
def app():
    """
    Create a new Flask app for testing.
    """
    # Assuming your Flask app instance is named 'app'
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite for tests

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield flask_app  # This will execute the test function

    # Teardown: the context is removed after the test runs
    ctx.pop()

@pytest.fixture(scope='module')
def client(app):
    """
    Create a test client from the Flask app.
    """
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    """
    Initialize the database.
    """
    with app.app_context():
        db.create_all()  # Create database tables for all models

    yield  # This will execute the test function

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Drop all tables after the test function has executed

@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test-api-key')

class TestGetUserDocuments:

    def test_returns_list_of_documents(self, client, init_database, mocker):
        mocker.patch('models.Document.query.filter_by', return_value=[Document(), Document()])
        response = client.get('/api/documents/user/user_id')
        assert isinstance(response.json, list)

    def test_returns_200_status_code(self, client, init_database, mocker):
        mocker.patch('models.Document.query.filter_by', return_value=[Document(), Document()])
        response = client.get('/api/documents/user/user_id')
        assert response.status_code == 200

    def test_returns_empty_list_if_no_documents_found(self, client, init_database, mocker):
        mocker.patch('models.Document.query.filter_by', return_value=[])
        response = client.get('/api/documents/user/user_id')
        assert response.json == []

# If needed, add additional tests below
