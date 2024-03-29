
import React, { useState } from 'react';
import Login from './components/Auth/Login';
import Dashboard from './components/Dashboard/Dashboard';
import credentials from './credentials.json';
import { jwtDecode } from 'jwt-decode'; // Corrected import statement
import { GoogleOAuthProvider } from '@react-oauth/google';
import { UserProvider, useUser } from './components/Auth/UserContext'
import { AppBar, Toolbar, Typography, Button, Container, Grid, CssBaseline, ThemeProvider, createTheme } from '@mui/material';

  
const theme = createTheme({
  palette: {
    primary: {
      main: '#556cd6',
    },
    secondary: {
      main: '#19857b',
    },
  },
});

const AppContent = () => {
  const [uploadTrigger, setUploadTrigger] = React.useState(false);
  const { user, login, logout } = useUser();
  
const [documents, setDocuments] = useState([]);


const handleAddNewDocument = (newDocObj) => {
  if (typeof newDocObj === 'object' && newDocObj.message && typeof newDocObj.message === 'string') {
    const prefix = 'Files queued for processing: ';
    if (newDocObj.message.startsWith(prefix)) {
      const filename = newDocObj.message.substring(prefix.length);
      setDocuments(currentDocs => [...currentDocs, { filename }]);
    }
  }
};



const fetchDocuments = async (userId) => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/documents/user/${userId}`);
    if (!res.ok) {
      const errorText = await res.text(); // Attempt to read the response text
      throw new Error(`Failed to fetch documents: ${res.status} ${errorText}`);
    }
    const data = await res.json();
    setDocuments(data); // Update the state with fetched documents
  } catch (error) {
    console.error('Error fetching documents:', error);
  }
};

const handleAuthSuccess = async (response) => {
  const decodedToken = jwtDecode(response.credential);
  login({
    sub: decodedToken.sub,
    name: decodedToken.name,
    email: decodedToken.email,
  });

  // Fetch user's documents
  await fetchDocuments(decodedToken.sub); // Now using fetchDocuments function
};



  const handleAuthFailure = (error) => {
    console.error('Authentication failed:', error);
    logout(); // Use logout from context
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Smart Document Analyzer
          </Typography>
          {!user ? (
            <Login onSuccess={handleAuthSuccess} onFailure={handleAuthFailure} />
          ) : (
            <Button color="inherit" onClick={logout}>Logout</Button>
          )}
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 3 }}>
        {user && (
          <>
            <Typography
              variant="h4" // Changed for a slightly larger size
              gutterBottom
              sx={{
                mt: 2,
                textAlign: 'center',
                color: 'deepSkyBlue',
                fontFamily: 'Arial', 
                fontWeight: 'bold',
              }}
            >
              Welcome, {user.name}!
            </Typography>
              <Button 
                color="primary" 
                variant="contained" 
                onClick={() => fetchDocuments(user.sub)} // Use the current user's sub for fetching
                sx={{ marginBottom: 2 }}
              >
                Refresh Documents
              </Button>
            <Grid container spacing={3}>
              <Grid item xs={12}><Dashboard documents={documents} onAddNewDocument={handleAddNewDocument} /></Grid>
            </Grid>
          </>
        )}
      </Container>


    </ThemeProvider>
  );
};

const App = () => (
  <GoogleOAuthProvider clientId={credentials.web.client_id}>
    <UserProvider> {/* UserProvider wraps AppContent now */}
      <AppContent />
    </UserProvider>
  </GoogleOAuthProvider>
);

export default App;