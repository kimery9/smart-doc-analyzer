import os

class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Directly use BASE_DIR since Config.BASE_DIR cannot be used within the class definition
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_if_none_found')
    # Define the endpoint for the login page
    # For example, if your login route is '/login', then LOGIN_VIEW = 'login'
    LOGIN_VIEW = 'login'
