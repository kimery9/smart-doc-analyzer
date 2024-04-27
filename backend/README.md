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


#### document_keywords:
##### Summary
This code defines a Flask route that filters paragraphs and sentences based on a given sentiment value.
#### Example Usage
```
GET /api/filter/sentiment/positive
```
#### Code Analysis
##### Inputs
- sentiment (string): The sentiment value to filter by.

###### Flow
1. Retrieve all paragraphs and sentences from the database that have the specified sentiment value.
2. Create a list of dictionaries containing the id, content, and sentiment of each paragraph.
3. Create a list of dictionaries containing the id, content, and sentiment of each sentence.
4. Return a JSON response containing the filtered paragraphs and sentences.
 
##### Outputs
JSON response containing the filtered paragraphs and sentences.


#### keyword_definition:
##### Summary

This code defines a Flask route `/keyword/definition` that accepts a POST request with a JSON payload containing a keyword parameter. The `keyword_definition` function retrieves the value of the keyword parameter from the request, calls the `get_keyword_definition` function to get the definition of the keyword using OpenAI's GPT-3.5 Turbo model, and returns a JSON response with the keyword and its definition.

##### Example Usage

```python
POST /keyword/definition
{
  "keyword": "python"
}
```

#### Code Analysis:
##### Inputs
- request.json: A JSON payload containing a keyword parameter.

##### Flow
1. Retrieve the keyword value from the JSON payload.
2. Check if the keyword value is empty. If it is, return a JSON response with an error message and a 400 status code.
3. Call the `get_keyword_definition` function with the keyword value to get the definition of the keyword.
4. Return a JSON response with the keyword and its definition.

##### Outputs
- JSON response with the keyword and its definition.


#### filter_by_sentiment:
##### Summary

This code defines a Flask route that filters paragraphs and sentences based on a given sentiment value.

##### Example Usage

```python
GET /api/filter/sentiment/positive
```
#### Code Analysis:
##### Inputs
- sentiment (string): The sentiment value to filter by.

##### Flow
1. Retrieve all paragraphs and sentences from the database that have the specified sentiment value.
2. Create a list of dictionaries containing the id, content, and sentiment of each paragraph.
3. Create a list of dictionaries containing the id, content, and sentiment of each sentence.
4. Return a JSON response containing the filtered paragraphs and sentences.

##### Outputs
- JSON response containing the filtered paragraphs and sentences.

#### log_error:
##### Summary

This function named `log_error` is currently empty and does not contain any code.

##### Example Usage

```python
log_error(exception)

#### Code Analysis:
##### Inputs
- e (exception): The input parameter e represents an exception that needs to be logged.

##### Flow
1. The function `log_error` does not have any code implementation. It is currently empty and does not perform any actions.

##### Outputs
- The function `log_error` does not have any output as it does not contain any code.


#### search_articles:
##### Summary

This code defines a Flask route named `/search` that handles a POST request. The function `search_articles` is executed when the route is accessed. It retrieves a keyword from the request JSON data, validates its format, and uses it to make a request to the Google Custom Search API. The API response is processed to extract the links of the search results, which are then returned as a JSON response.

##### Example Usage

```python
POST /search
{
  "keyword": "python tutorial"
}
```
#### Code Analysis:
##### Inputs
- keyword (string): The keyword to search for.

##### Flow
1. Retrieve the keyword from the request JSON data.
2. If the keyword is missing, return a JSON response with an error message and status code 400.
3. Validate the format of the keyword using a regular expression. If it is not alphanumeric or contains special characters, return a JSON response with an error message and status code 400.
4. Create a dictionary `params` with the necessary parameters for the Google Custom Search API request: `key` (API key), `cx` (custom search engine ID), and `q` (search query).
5. Make a GET request to the Google Custom Search API with the specified parameters.
6. If the API response status code is 200 (success), extract the links of the search results from the JSON response.
7. Return a JSON response with the keyword and the extracted links.
8. If the API response status code is not 200, return a JSON response with an error message and the response status code.

##### Outputs
- JSON response with the keyword and the links of the search results, or an error message and status code.


#### search_by_keyword:
##### Summary

This code defines a Flask API endpoint `/api/search/keyword` that allows users to search for sentences and paragraphs containing a specific keyword. The function `search_by_keyword` retrieves the keyword from the request JSON, performs a database query to find all sentences containing the keyword, retrieves the corresponding paragraphs, and returns the sentences and paragraphs as JSON response.

##### Example Usage

```python
POST /api/search/keyword
{
  "keyword": "python"
}
```
#### Code Analysis:
##### Inputs
- keyword (string): The keyword to search for in the sentences and paragraphs.

##### Flow
1. Retrieve the keyword from the request JSON.
2. If the keyword is not provided, return a JSON response with an error message.
3. Perform a database query to find all sentences that contain the keyword.
4. Retrieve the IDs of the matching sentences.
5. Perform another database query to find the paragraphs that contain the matching sentences.
6. Create a list of dictionaries containing the IDs and content of the matching sentences.
7. Create a list of dictionaries containing the IDs and content of the paragraphs that contain the matching sentences.
8. Return a JSON response containing the lists of matching sentences and paragraphs.

##### Outputs
- JSON response containing the sentences and paragraphs that match the keyword. The response has the following structure:
```json
{
  "sentences": [
    {
      "id": 1,
      "content": "This is a sentence containing the keyword."
    },
    ...
  ],
  "paragraphs": [
    {
      "id": 1,
      "content": "This is a paragraph containing the keyword."
    },
    ...
  ]
}
```

#### get_document_summary:
##### Summary

This code defines a function named `get_document_summary` that takes a document text as input and uses the OpenAI API to generate a summary of the document. The function makes a chat completion request to the API, providing a system message and a user message containing the document text. It uses the "gpt-3.5-turbo" model for generating the summary. If an error occurs during the API request, the function prints the error message and raises an exception.

###### Example Usage

```python
document_text = "This is the content of the document."
summary = get_document_summary(document_text)
print(summary)
```
#### Code Analysis:
##### Inputs
- document_text (string): The text of the document for which a summary is to be generated.
##### Flow
1. The function takes the document_text as input.
2. It creates a chat completion request to the OpenAI API, providing a system message and a user message containing the document_text.
3. The API generates a summary of the document using the "gpt-3.5-turbo" model
4. The function returns the generated summary.
##### Outputs
- summary (string): The generated summary of the document.


#### get_keyword_definition:
##### Summary

This code defines a function named `get_keyword_definition` that takes a keyword as input and uses the OpenAI API to generate a definition for the keyword. The function sends a chat completion request to the API with a system message and a user message containing the keyword. It then returns the generated definition.

###### Example Usage

```python
keyword = "example"
definition = get_keyword_definition(keyword)
print(definition)
```
#### Code Analysis:
##### Inputs
- keyword (string): The keyword for which the definition is to be generated.
##### Flow
1. The function receives a keyword as input.
2. It creates a chat completion request to the OpenAI API with a system message stating that it is an intelligent assistant and a user message asking to define the keyword.
3. The function sends the completion request to the API using the `client.chat.completions.create` method.
4. It retrieves the generated completion from the API response.
5. The function returns the content of the first choice in the completion as the definition.
##### Outputs
- definition (string): The generated definition for the keyword.


#### analyze_sentiment:
##### Summary

The `analyze_sentiment` function performs sentiment analysis on a given text using the TextBlob library.

###### Example Usage

```python
text = "I love this product!"
sentiment = analyze_sentiment(text)
print(sentiment)
```

#### Code Analysis:
##### Inputs
- text (string): The text to be analyzed for sentiment.

##### Flow
1. Create a TextBlob object from the input text.
2. Calculate the polarity of the text using the `sentiment.polarity` attribute of the TextBlob object.
3. If the polarity is greater than 0, return "positive".
4. If the polarity is less than 0, return "negative".
5. If the polarity is 0, return "neutral".

##### Outputs
- sentiment (string): The sentiment of the input text, which can be "positive", "negative", or "neutral".



#### split_into_paragraphs:
##### Summary

This function takes a string of text as input and splits it into paragraphs based on the occurrence of double newline characters ('\n\n').

###### Example Usage

```python
text = "This is the first paragraph.\n\nThis is the second paragraph.\n\nThis is the third paragraph."
paragraphs = split_into_paragraphs(text)
print(paragraphs)
```

#### Code Analysis:
##### Inputs
- text (string): The input text that needs to be split into paragraphs.

##### Flow
1. The function takes a string of text as input.
2. It splits the text into paragraphs by using the `split()` method with the delimiter '\n\n', which represents double newline characters.
3. The resulting paragraphs are returned as a list.

##### Outputs
- paragraphs (list): A list of paragraphs obtained by splitting the input text based on double newline characters.



#### split_into_sentences:
##### Summary

The `split_into_sentences` function takes a paragraph as input and uses the spaCy library to split the paragraph into individual sentences.

###### Example Usage

```python
paragraph = "This is the first sentence. This is the second sentence."
sentences = split_into_sentences(paragraph)
print(sentences)
```
Output:
['This is the first sentence.', 'This is the second sentence.']

#### Code Analysis:
##### Inputs
- paragraph (string): The paragraph that needs to be split into sentences.

##### Flow
1. The function takes a paragraph as input.
2. It passes the paragraph to the spaCy `nlp` object, which processes the text and returns a `Doc` object.
3. The `Doc` object is iterated over, and each sentence is extracted using the `sents` attribute.
4. The text of each sentence is appended to a list.
5. The list of sentences is returned as the output.

##### Outputs
- List of sentences: Each sentence in the paragraph is extracted and returned as a separate string element in a list.



#### extract_keywords:
##### Summary

The `extract_keywords` function takes a sentence as input and uses the spaCy library to extract keywords from the sentence. It returns a list of lemmatized nouns and proper nouns.

###### Example Usage

```python
sentence = "The quick brown fox jumps over the lazy dog."
keywords = extract_keywords(sentence)
print(keywords)
```
Output:
['fox', 'dog']

#### Code Analysis:
##### Inputs
- sentence (string): The input sentence from which keywords need to be extracted.

##### Flow
1. The function takes a sentence as input.
2. It uses the spaCy library to process the sentence and create a spaCy `Doc` object.
3. It iterates over each token in the `Doc` object.
4. For each token, it checks if the part-of-speech tag is either 'NOUN' or 'PROPN' (noun or proper noun).
5. If the token's part-of-speech tag matches, it retrieves the lemma (base form) of the token and adds it to the list of keywords.
6. Finally, it returns the list of extracted keywords.

##### Outputs
- keywords (list): A list of lemmatized nouns and proper nouns extracted from the input sentence.



#### extract_text_from_pdf:
##### Summary

This code defines a function named `extract_text_from_pdf` that takes a file path as input and returns the extracted text from a PDF file. It uses the fitz library to open the PDF file and iterate over its pages to extract the text.

###### Example Usage

```python
result = extract_text_from_pdf("path/to/file.pdf")
print(result)
```

#### Code Analysis:
##### Inputs
- filepath: a string representing the path to the PDF file.

##### Flow
1. Import the fitz library.
2. Initialize an empty string variable named `text`.
3. Try to open the PDF file using `fitz.open(filepath)`.
4. Iterate over each page in the document.
5. Get the text content of each page using `page.get_text()` and append it to the `text` variable.
6. If any exception occurs during the process, print an error message.
7. Return the extracted text.

##### Outputs
- text: a string representing the extracted text from the PDF file.



#### extract_text_from_image:
##### Summary

The `extract_text_from_image` function takes a file path as input and uses the pytesseract library to perform optical character recognition (OCR) on the image file. It returns the extracted text from the image.

###### Example Usage

```python
result = extract_text_from_image('image.jpg')
print(result)
```
Output:
Text from image

#### Code Analysis:
##### Inputs
- filepath: a string representing the path to the image file.

##### Flow
1. The function opens the image file using the `Image.open` function from the PIL library.
2. It then uses the `pytesseract.image_to_string` function to perform OCR on the opened image and extract the text.
3. The extracted text is returned as the result.

##### Outputs
- A string representing the extracted text from the image.


#### extract_text_from_txt:
##### Summary

This function extracts text from a .txt file.

###### Example Usage

```python
filepath = 'path/to/file.txt'
text = extract_text_from_txt(filepath)
print(text)
```

#### Code Analysis:
##### Inputs
- filepath: a string representing the path to the .txt file.

##### Flow
1. Open the .txt file specified by `filepath` using the `open()` function.
2. Read the contents of the file using the `read()` method.
3. Store the text content in the `text` variable.
4. Close the file.
5. Return the extracted text.

##### Outputs
- text: a string containing the extracted text from the .txt file.


#### extract_text_from_docx:
##### Summary

This function extracts text from a .docx file by using the python-docx library. It returns the text content of all paragraphs in the document, excluding empty paragraphs.

###### Example Usage

```python
filepath = "path/to/document.docx"
text = extract_text_from_docx(filepath)
print(text)
```

#### Code Analysis:
##### Inputs
- filepath (string): The path to the .docx file.

##### Flow
1. The function takes the `filepath` as input.
2. It tries to open the .docx file using the `DocxDocument` class from the python-docx library.
3. It iterates over all paragraphs in the document and extracts the text content of each paragraph using a list comprehension.
4. The extracted text is joined with newline characters ('\n') to create a single string.
5. The function returns the joined string of paragraph texts.

##### Outputs
- text (string): The extracted text content from the .docx file.


