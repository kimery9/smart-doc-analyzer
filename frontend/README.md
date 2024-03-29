# Frontend for Smart Document Analyzer

This frontend application interacts with the Smart Document Analyzer backend to upload documents, display uploaded documents, fetch summaries, keywords, and allow filtering by sentiment or keyword. It's built using React and Ant Design for UI components, with Axios for making HTTP requests.

## Getting Started

### Prerequisites

- Node.js (v14 or later recommended)
- npm (usually comes with Node.js)
- Backend API running (refer to the backend README for setup instructions)

### Installation

1. Clone the repository to your local machine.
2. Navigate to the frontend directory where the `package.json` file is located.
3. Install the required npm packages:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm start
   ```
   This will run the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### Environment Variables

Before running the application, ensure you have the correct environment variables set up for connecting to your backend API and any other external services (if applicable). Create a `.env` file in the root of your frontend project folder with the necessary variables, for example:
```
REACT_APP_API_URL=http://127.0.0.1:5000
```

### Running with Docker

To containerize and run the frontend application using Docker, follow these steps:

1. Ensure Docker is installed on your machine.
2. Build the Docker image:
   ```
   docker build -t yourfrontendapp .
   ```
3. Run the Docker container:
   ```
   docker run -p 3000:3000 yourfrontendapp
   ```

## Features

- **Document Upload:** Users can select and upload documents. The uploader supports multiple file formats and displays the upload progress.
- **Document List:** Displays a list of uploaded documents with options to view summaries and keywords.
- **Search and Filtering:** Provides functionality to filter documents by sentiment or search by keywords.
- **Authentication:** Integrates with Google OAuth for user authentication and session management.

## Components Overview

- `DocumentUploader`: Allows users to upload files and handles the upload logic.
- `DocumentList`: Displays uploaded documents and fetches summaries or keywords on demand.
- `Dashboard`: Main component that includes `DocumentUploader` and `DocumentList`, orchestrating the user interactions.
- `Login` and `UserContext`: Manage user authentication and provide user context throughout the app.

## Docker Deployment

The provided Dockerfile containerizes the React app for production deployment. It builds the app with `npm run build` and serves it using `serve`.
