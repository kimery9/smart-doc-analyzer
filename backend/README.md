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

## Function explanations:

#### process_file_from_queue:
##### Summary

This code defines a function named `process_file_from_queue` that continuously processes files from a queue. It extracts text from different file types (PDF, image, text, and docx), performs sentiment analysis on the extracted text, and stores the results in a database.

###### Example Usage

```python
# Add a file to the processing queue
file_processing_queue.put((filepath, filename, user_id))
# Start processing files from the queue
process_file_from_queue()
```
#### Code Analysis:
###### Inputs
- filepath (string): The path to the file to be processed.
- filename (string): The name of the file to be processed.
- user_id (string): The ID of the user who uploaded the file.

###### Flow
1. The function continuously loops and waits for a file processing task from the queue.
2. Once a task is received, the filepath, filename, and user_id are unpacked from the task.
3.The process_file function is called with the filepath, filename, and user_id as arguments.
4. The process_file function extracts text from the file based on its extension (PDF, image, text, or docx).
5. The extracted text is split into paragraphs, and for each paragraph, it is further split into sentences.
6. Sentiment analysis is performed on each sentence, and keywords are extracted from each sentence.
7. The extracted text, sentiment, and keywords are stored in the database.
8. The function continues to wait for the next file processing task.
##### Outputs
None. The function continuously processes files from the queue.

#### process_file:
##### Summary
This code defines a function called process_file that takes a file path, file name, and user ID as inputs. The function extracts text from different file formats such as PDF, images, text files, and Word documents. It then performs sentiment analysis on the extracted text and stores the results in a database using SQLAlchemy.
##### Example Usage
```
process_file('/path/to/file.pdf', 'file.pdf', 1)
```
#### Code Analysis
##### Inputs
- filepath: A string representing the path to the file.
- filename: A string representing the name of the file.
- user_id: An integer representing the ID of the user.
 
##### Flow
1. The function checks the file extension of the filename to determine the file format.
2. If the file is a PDF, it calls the extract_text_from_pdf function to extract the text from the PDF file.
3. If the file is an image (PNG, JPG, JPEG, or GIF), it calls the extract_text_from_image function to extract the text from the image.
4. If the file is a text file (TXT), it calls the extract_text_from_txt function to extract the text from the text file.
5. If the file is a Word document (DOCX), it calls the extract_text_from_docx function to extract the text from the Word document.
6. The extracted text is stored in the full_text variable.
7. The sentiment of the full_text is analyzed using the analyze_sentiment function.
8. A new Document object is created with the content, sentiment, filename, and user_id attributes.
9. The Document object is added to the database session.
10. The full_text is split into paragraphs using the split_into_paragraphs function.
11. For each paragraph, a new Paragraph object is created with the document, content, and sentiment attributes.
12. The Paragraph object is added to the database session
13. Each paragraph is split into sentences using the split_into_sentences function.
14. For each sentence, a new Sentence object is created with the paragraph, content, and sentiment attributes.
15. The Sentence object is added to the database session.
16. Keywords are extracted from each sentence using the extract_keywords function
17. For each keyword, a new Keyword object is created with the sentence and word attributes.
18. The Keyword object is added to the database session.
19. The changes are committed to the database.
20. The function returns a JSON response with a success message and the sentiment of the document.
 
##### Outputs
A JSON response containing a success message and the sentiment of the document.

#### upload_file:
##### Summary
This code defines a Flask route /upload that handles file uploads. It checks if a userId is provided and if files are selected. It then processes each file, checking if it has an allowed file extension and saving it to a specified folder. The file details, including the userId, are added to a queue for further processing. Finally, it returns a response indicating the files that have been queued for processing.

##### Example Usage
```
# Upload a file with a userId
data = {
    'file': (io.BytesIO(b"Fake file content"), 'test.pdf'),
    'userId': '1'
}
response = client.post('/upload', data=data, content_type='multipart/form-data')

# Expected output: 202 - Files queued for processing: test.pdf

# Upload a file without a userId
data = {
    'file': (io.BytesIO(b"Fake file content"), 'test.pdf')
}
response = client.post('/upload', data=data, content_type='multipart/form-data')

# Expected output: 400 - UserId is required

# Upload a file with an unsupported file type
data = {
    'file': (io.BytesIO(b"Fake file content"), 'test.xyz'),
    'userId': '1'
}
response = client.post('/upload', data=data, content_type='multipart/form-data')

# Expected output: 400 - File type not allowed
```
#### Code Analysis
##### Inputs
- files: A list of files uploaded by the user.
- userId: The ID of the user who uploaded the files.
 
##### Flow
1. Check if userId is provided. If not, return an error response indicating that userId is required
2. Check if any files are selected. If not, return an error response indicating that no files are selected
3. Iterate over each file in the files list.
4. Check if the file has an allowed file extension
5. If the file has an allowed file extension, secure the filename and save the file to a specified folder.
6. Add the file details, including the userId, to a queue for further processing.
7. Append the filename to the processed_files list.
8. If no valid files were processed, return an error response indicating that no valid files were processed.
9. Return a success response indicating the files that have been queued for processing.
 
##### Outputs
- Success response: A JSON response with a status code of 202 and a message indicating the files that have been queued for processing.
- Error response (UserId is required): A JSON response with a status code of 400 and an error message indicating that userId is required.
- Error response (No files selected): A JSON response with a status code of 400 and an error message indicating that no files are selected.
- Error response (File type not allowed): A JSON response with a status code of 400 and an error message indicating that the file type is not allowed.

#### get_user_documents:
##### Summary
This code defines a Flask route that retrieves all documents associated with a specific user. It returns a JSON response containing the filenames, document IDs, and sentiment scores of the documents.
##### Example Usage
```
GET /api/documents/user/123456
```
#### Code Analysis
##### Inputs
- user_id (string): The ID of the user whose documents are to be retrieved.
 
##### Flow
1. Retrieve all documents from the database that have a matching user_id
2. Create a list comprehension to extract the filename, document ID, and sentiment score for each document.
3. Return a JSON response containing the extracted data.
 
##### Outputs
documents_data (JSON): A JSON response containing the filenames, document IDs, and sentiment scores of the retrieved documents.


#### document_summary:
##### Summary
The document_summary function is a Flask route that handles a POST request to '/document/summary'. It retrieves the filename from the request data, queries the database for a document with that filename, and generates a summary of the document using the get_document_summary function. The summary is then returned as a JSON response.

##### Example Usage
```
POST /document/summary
{
  "filename": "example_document.txt"
}
```
#### Code Analysis
##### Inputs
- filename: a string representing the filename of the document to summarize.
##### Flow
1. Retrieve the filename from the request data.
2. Query the database for a document with the specified filename.
3. If the document is not found, return a JSON response with an error message.
4. Generate a summary of the document using the get_document_summary function.
5. Return a JSON response with the filename and the generated summary.
 
##### Outputs
JSON response with the filename and the generated summary.


####document_keywords

 
