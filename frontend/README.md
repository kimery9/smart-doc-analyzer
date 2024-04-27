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

## Function Explanations:
#### App:
##### Summary

The `App` function is the main component of the application. It renders the GoogleOAuthProvider component from the @react-oauth/google library, which provides the authentication functionality. It also wraps the AppContent component with the UserProvider component, which manages the user state and provides the login and logout functions.

###### Example Usage

```javascript
import React from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { UserProvider } from './components/Auth/UserContext';
import AppContent from './AppContent';

const App = () => (
  <GoogleOAuthProvider clientId={credentials.web.client_id}>
    <UserProvider>
      <AppContent />
    </UserProvider>
  </GoogleOAuthProvider>
);
```

#### Code Analysis:
##### Inputs
- None

##### Flow
1. The App component is a functional component that renders the GoogleOAuthProvider component.
2. The GoogleOAuthProvider component is imported from the @react-oauth/google library and takes a clientId prop, which is provided from the credentials.json file.
3. The UserProvider component is imported from the ./components/Auth/UserContext file and wraps the AppContent component.
4. The AppContent component is imported from the ./AppContent file and is rendered inside the UserProvider component.
5. The AppContent component contains the main content of the application, including the authentication logic and the user interface.

##### Outputs
- The rendered application with authentication and user interface components.


#### AppContent:
##### Summary

This code defines the `AppContent` function, which is a React component responsible for rendering the main content of the application. It handles user authentication, displays the user's name, and allows the user to fetch and display their documents.

###### Example Usage

```jsx
<AppContent />
```

#### Code Analysis:
##### Inputs
- None

##### Flow
1. The `AppContent` component initializes state variables using the `useState` hook.
2. It retrieves the user, login, and logout functions from the `useUser` hook.
3. It defines a function `handleAddNewDocument` to handle adding new documents to the state.
4. It defines a function `fetchDocuments` to fetch the user's documents from the server.
5. It defines a function `handleAuthSuccess` to handle successful authentication.
6. It defines a function `handleAuthFailure` to handle authentication failure.
7. The component renders the application's UI using Material-UI components.
8. It conditionally renders the login button or the logout button based on the user state.
9. It renders the user's name and a button to refresh the documents if the user is logged in.
10. It renders the `Dashboard` component to display the user's documents.
11. The component returns the rendered UI.

##### Outputs
- The rendered UI of the `AppContent` component.


#### OAuthLogin:
##### Summary

This code defines a React component called `OAuthLogin` that renders a Google login button. It uses the GoogleLogin component from the @react-oauth/google library and requires a clientId prop to be passed in. The onSuccess and onFailure props are callbacks that handle the login result.

###### Example Usage

```jsx
import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import credentials from '../../credentials.json';

const OAuthLogin = ({ onSuccess, onFailure }) => {
    const { web: { client_id } } = credentials;

    return (
        <GoogleLogin
            clientId={client_id}
            onSuccess={onSuccess}
            onError={onFailure}
            render={renderProps => (
                <button onClick={renderProps.onClick} disabled={renderProps.disabled}>
                    Login with Google
                </button>
            )}
        />
    );
};
```

#### Code Analysis:
##### Inputs
- onSuccess: A callback function to be called when the login is successful.
- onFailure: A callback function to be called when the login fails.

##### Flow
1. Extract the client_id from the credentials object.
2. Render the GoogleLogin component with the clientId, onSuccess, onFailure, and render props.
3. The render prop is a function that receives renderProps as an argument.
4. Render a button with an onClick event handler that calls renderProps.onClick and a disabled attribute that is set to renderProps.disabled.
5. Return the GoogleLogin component.

##### Outputs
- The rendered Google login button component.



#### useUser:
##### Summary

The `useUser` function is a custom hook in React that allows components to access the user context provided by the UserContext context object.

###### Example Usage

```javascript
import { useUser } from './useUser';

function MyComponent() {
  const user = useUser();

  // Use the user object here
  // ...

  return (
    // JSX code here
  );
}
```

#### Code Analysis:
##### Inputs
There are no inputs for the `useUser` function. It is a custom hook that uses the `useContext` hook from React.

##### Flow
1. The `useUser` function imports the `useContext` hook and the `UserContext` context object from React.
2. It defines a custom hook named `useUser` that returns the result of calling `useContext(UserContext)`.
3. The `useUser` hook can be used in any component that is a descendant of the `UserContext.Provider` component. It allows components to access the user context value provided by the `UserContext.Provider`.
4. When a component calls the `useUser` hook, it will receive the current value of the user context.

##### Outputs
The `useUser` function returns the current value of the user context provided by the `UserContext.Provider` component. This allows components to access the user context value and use it in their rendering or logic.



#### UserProvider:
##### Summary

This code defines a React context called `UserContext` and exports a component called `UserProvider`. The `UserProvider` component is responsible for managing the state of the user and providing it to its child components through the `UserContext`.

###### Example Usage

```javascript
import { UserProvider } from './UserProvider';

function App() {
  return (
    <UserProvider>
      {/* Your app components */}
    </UserProvider>
  );
}
```

#### Code Analysis:
##### Inputs
- children: The child components that will have access to the user state and functions.

##### Flow
1. The `UserProvider` component is imported and used in the parent component.
2. The `UserProvider` component receives the `children` prop.
3. Inside the `UserProvider` component, a state variable called `user` is initialized with a value of `null` using the `useState` hook.
4. Two functions, `login` and `logout`, are defined. The `login` function takes a `userDetails` parameter and sets the `user` state to the provided value. The `logout` function sets the `user` state back to `null`.
5. The `UserContext.Provider` component is rendered with a `value` prop that contains the `user` state, `login` function, and `logout` function.
6. The children components are rendered as the children of the `UserContext.Provider` component.

##### Outputs
The `UserProvider` component provides the user state, login function, and logout function to its child components through the `UserContext`.



#### Dashboard:
##### Summary

The `Dashboard` function is a React component that renders a dashboard for managing documents. It includes a `DocumentUploader` component for uploading new documents and a `DocumentList` component for displaying the uploaded documents.

###### Example Usage

```jsx
import React from 'react';

const Dashboard = ({ documents, onAddNewDocument }) => {
return (
<div>
<h2>Dashboard</h2>
<DocumentUploader onAddNewDocument={onAddNewDocument} />
<DocumentList documents={documents} />
</div>
);
};

export default Dashboard;
```

#### Code Analysis:
##### Inputs
- documents (array): An array of objects representing the uploaded documents.
- onAddNewDocument (function): A callback function to handle adding a new document.

##### Flow
1. The `Dashboard` component receives the `documents` array and the `onAddNewDocument` callback function as props.
2. It renders a heading for the dashboard and the `DocumentUploader` component.
3. When a new document is uploaded using the `DocumentUploader` component, the `onNewDocument` callback is called with the new document object.
4. The `onAddNewDocument` callback function is passed as a prop to the `DocumentUploader` component to handle adding the new document to the list of documents.
5. The `DocumentList` component is rendered with the `documents` array as a prop to display the uploaded documents.

##### Outputs
The rendered dashboard component.



#### KeywordArticles:
##### Summary

The `KeywordArticles` function is a React component that displays a list of keywords and allows the user to fetch related articles for each keyword. It uses the `useState` hook to manage the state of the selected keyword, fetched articles, and error messages. The function also makes an HTTP request to a backend server to fetch the articles based on the selected keyword.

###### Example Usage

```jsx
<KeywordArticles keywords={["keyword1", "keyword2", "keyword3"]} />
```

#### Code Analysis:
##### Inputs
- keywords (array): An array of keywords for which the user wants to fetch related articles.

##### Flow
1. The `KeywordArticles` component receives the `keywords` prop.
2. It initializes the state variables `selectedKeyword`, `articles`, and `error` using the `useState` hook.
3. When a keyword button is clicked, the `fetchArticles` function is called with the selected keyword as an argument.
4. The `fetchArticles` function makes an HTTP POST request to the backend server with the selected keyword.
5. If the request is successful, the fetched articles are stored in the `articles` state variable, the selected keyword is updated, and the error message is cleared.
6. If the request fails, an error message is displayed and the `articles` state variable is cleared.

##### Outputs
- The rendered component displays a list of buttons, each representing a keyword.
- When a keyword button is clicked, the component makes an HTTP request to fetch related articles for that keyword.
- The fetched articles are displayed as clickable links.
- If no articles are found for a keyword, a message indicating that no articles were found is displayed.
- If there is an error fetching the articles, an error message is displayed.



#### DocumentList:
##### Summary

The `DocumentList` function is a React component that displays a list of uploaded documents. It allows the user to fetch the summary and keywords for each document, as well as filter the displayed sentences and paragraphs based on sentiment or keyword.

###### Example Usage

```jsx
<DocumentList documents={documents} />
```

#### Code Analysis:
##### Inputs
- documents (array): An array of objects representing the uploaded documents. Each object should have a `filename` and `sentiment` property.

##### Flow
1. The function initializes state variables for the selected document, summary, keywords, error, search keyword, filtered sentences, and filtered paragraphs.
2. The function defines helper functions to fetch the summary, keywords, and filtered data based on sentiment or keyword.
3. When the user clicks on the "Get Summary" button for a document, the `fetchSummary` function is called. It sends a POST request to the server to fetch the summary for the selected document. If successful, it updates the state variables for summary, selected document, keywords, and error.
4. When the user clicks on the "Show Keywords" button for a document, the `fetchKeywords` function is called. It sends a POST request to the server to fetch the keywords for the selected document. If successful, it updates the state variables for keywords, selected document, and error.
5. When the user enters a keyword in the search input and clicks the "Search" button, the `fetchByKeyword` function is called. It sends a POST request to the server to fetch the sentences and paragraphs containing the specified keyword. If successful, it updates the state variables for filtered sentences, filtered paragraphs, summary, keywords, and error.
6. When the user selects a sentiment filter from the dropdown menu, the `fetchFilteredBySentiment` function is called. It sends a GET request to the server to fetch the sentences and paragraphs with the specified sentiment. If successful, it updates the state variables for filtered sentences, filtered paragraphs, summary, keywords, and error.
7. The function renders the list of documents using the `List` component from the Ant Design library. Each document is displayed with its filename and sentiment.
8. When the user clicks on the "Get Summary" or "Show Keywords" button for a document, the corresponding summary, keywords, and keyword articles are displayed if the selected document matches the clicked document.
9. If there are filtered sentences or paragraphs, they are displayed below the document list.

##### Outputs
None. The function is a React component and does not return any value.




#### DocumentSummary:
##### Summary

The `DocumentSummary` function is a React component that renders a card containing the summary of a document. It takes two props, `summary` and `filename`, and displays the summary along with the filename in a card.

###### Example Usage

```jsx
<DocumentSummary summary="This is the summary of the document" filename="example.docx" />
```

This will render a card with the title "Summary for example.docx" and the content "This is the summary of the document".

#### Code Analysis:
##### Inputs
- summary (string): The summary of the document.
- filename (string): The name of the document.

##### Flow
1. The `DocumentSummary` component receives the `summary` and `filename` props.
2. It renders a `Card` component with a title and a paragraph.
3. The title displays "Summary for {filename}".
4. The paragraph displays the `summary` prop.

##### Outputs
The `DocumentSummary` component renders a card containing the summary of a document.



#### DocumentUploader:
##### Summary

The `DocumentUploader` function is a React component that allows users to upload multiple files. It handles the file selection, file upload, and displays a loading spinner while the upload is in progress. It also provides error handling and displays success messages upon successful upload.

###### Example Usage

```jsx
<DocumentUploader onNewDocument={handleNewDocument} />
```

#### Code Analysis:
##### Inputs
- `onNewDocument`: a function that is called when a new document is uploaded. It takes the uploaded document as an argument.

##### Flow
1. The component initializes the state variables `fileList` and `uploading` using the `useState` hook.
2. The `beforeUpload` function is called when a file is selected for upload. It adds the selected file to the `fileList` state variable and prevents automatic upload.
3. The `handleUpload` function is called when the user clicks the "Start Upload" button. It performs validation checks on the `fileList` and the user's ID.
4. If the validation checks pass, the `handleUpload` function sets the `uploading` state variable to true and creates a FormData object to store the selected files and the user's ID.
5. The function sends a POST request to the server with the FormData object as the request body.
6. If the response from the server is successful, the function calls the `onNewDocument` function with the uploaded document as an argument, displays a success message, and clears the `fileList`.
7. If the response from the server is not successful, the function displays an error message.
8. Finally, the `uploading` state variable is set back to false.

##### Outputs
None. The `DocumentUploader` component is responsible for handling the file upload process and displaying relevant messages to the user.



#### KeywordList:
##### Summary

The `KeywordList` function is a React component that displays a list of keywords for a specific document. It also allows the user to fetch the definition of each keyword by clicking on it.

###### Example Usage

```jsx
<DocumentList keywords={["keyword1", "keyword2"]} filename="document1" />
```
#### Code Analysis:
##### Inputs
- `keywords` (array): An array of keywords to be displayed.
- `filename` (string): The name of the document for which the keywords are being displayed.

##### Flow
1. The `KeywordList` component receives the `keywords` and `filename` as props.
2. It initializes the `definitions` state as an empty object and the `err` state as null.
3. The `fetchKeywordDefinition` function is defined to fetch the definition of a keyword.
4. When rendering the component, it displays the heading "Keywords for {filename}".
5. If there is an error (`err` is not null), it displays the error message.
6. It renders a list of keywords using the List component from the antd library.
7. Each keyword is rendered as a list item.
8. The keyword is displayed as a button, and when clicked, it calls the `fetchKeywordDefinition` function.
9. The `fetchKeywordDefinition` function checks if the definition for the keyword is already fetched (`definitions[keyword]` exists).
10. If the definition is already fetched, it returns early to avoid refetching.
11. If the definition is not fetched, it makes a POST request to the server to fetch the definition.
12. The fetched definition is stored in the `definitions` state using the keyword as the key.
13. If there is an error during the fetch, it sets the `err` state with an error message.

##### Outputs
The rendered list of keywords for the specified document.
The ability to fetch the definition of each keyword by clicking on it.


#### SearchBar:
##### Summary

The `SearchBar` function is a React component that renders a search bar with dropdown menus and a search button. It uses the useState hook to manage the state of the search term, sentiment, and filter options. When the search button is clicked, it makes an asynchronous POST request to a search endpoint using the axios library. The response data, which is assumed to be an array of documents or excerpts, is then passed to the `onSearchResult` callback function.

###### Example Usage
```jsx
<SearchBar onSearchResult={handleSearchResult} />
```
#### Code Analysis
##### Inputs
- `onSearchResult` (function): A callback function that will be called with the search results.

##### Flow
1. The `SearchBar` component renders an input field for the search term, two dropdown menus for sentiment and filter options, and a search button.
2. When the search term input field is changed, the `setSearchTerm` function is called to update the `searchTerm` state.
3. When the sentiment dropdown menu is changed, the `setSentiment` function is called to update the `sentiment` state.
4. When the filter dropdown menu is changed, the `setFilter` function is called to update the `filter` state.
5. When the search button is clicked, the `handleSearch` function is called.
6. Inside the `handleSearch` function, an asynchronous POST request is made to the 'http://localhost:5000/search' endpoint with the `searchTerm`, `sentiment`, and `filter` as the request payload.
7. If the request is successful, the response data is passed to the `onSearchResult` callback function.
8. If the request fails, an error message is logged to the console.

##### Outputs
- None. The `SearchBar` component does not have any direct outputs. The search results are passed to the `onSearchResult` callback function.




