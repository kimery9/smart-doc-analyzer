## Description

This project provides a web application for document processing and sentiment analysis. It allows users to upload documents in various formats (PDF, DOCX, TXT, PNG, JPG, JPEG, GIF), performs text extraction, sentiment analysis at the document, paragraph, and sentence levels, and keyword extraction. It uses Flask for the backend, SQLAlchemy for ORM, PyMuPDF for PDF processing, Tesseract for OCR, TextBlob for sentiment analysis, and spaCy for text manipulation. OpenAI's API is used for generating summaries and keyword definitions.

## Getting Started

### Dependencies

- Python 3.8+
- Flask, SQLAlchemy, Flask-Migrate, Flask-CORS
- PyMuPDF, Pillow, pytesseract, TextBlob, spaCy, python-docx
- OpenAI API key for accessing OpenAI services
- A Google API key and CX for using Google Custom Search
- Docker (optional for containerization)

### Setting Up

1. Clone the repository to your local machine.
2. Install the required Python packages by running:
   ```
   pip install -r requirements.txt
   ```
3. Ensure `tesseract.exe` is installed and correctly set in `app.py` for OCR functionalities.
4. Set up environment variables including `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and `GOOGLE_CX` in a `.env` file based on your OpenAI and Google API credentials.

### Running the Application

1. To start the Flask application, navigate to the project directory and run:
   ```
   flask run
   ```
2. For deploying with Docker, ensure Docker is installed and run:
   ```
   docker build -t yourappname .
   docker run -p 5000:5000 yourappname
   ```
   Adjust `yourappname` as needed.

## Features

- File upload and processing queue system for handling multiple document formats.
- Text extraction from PDFs, images, text files, and DOCX documents.
- Sentiment analysis on different levels (document, paragraph, sentence) using TextBlob.
- Keyword extraction from sentences using spaCy.
- Integration with OpenAI for document summarization and keyword definitions.
- User authentication using Flask-Login and Flask-Dance for Google OAuth.
- RESTful API endpoints for document management and search functionalities.

## API Endpoints

Here's a brief overview of the provided API endpoints:

- `/upload` - For uploading files for processing.
- `/api/documents/user/<user_id>` - To retrieve documents associated with a user.
- `/document/summary` - To get a summary of a document.
- `/document/keywords` - To retrieve keywords from a document.
- Additional endpoints for document search, keyword definitions, and sentiment filtering.
