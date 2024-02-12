from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        if password is not None:
            self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Assuming your user table is named 'user'
    user = db.relationship('User', backref='documents')
    filename = db.Column(db.String(256), unique=True, nullable=False)  # Added filename attribute
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)  # Assuming you've a way to calculate this
    paragraphs = db.relationship('Paragraph', backref='document', lazy=True)

class Paragraph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)
    sentences = db.relationship('Sentence', backref='paragraph', lazy=True)

class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = db.Column(db.Integer, db.ForeignKey('paragraph.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)
    keywords = db.relationship('Keyword', backref='sentence', lazy=True)

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'), nullable=False)
    word = db.Column(db.String(255), nullable=False)




    def __repr__(self):
        return f"<Document {self.filename}>"
