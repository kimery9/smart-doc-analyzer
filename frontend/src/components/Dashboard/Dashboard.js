import React, { useState } from 'react';
import DocumentUploader from '../DocumentUploader/DocumentUploader'; // We'll create this next
import DocumentList from '../DocumentList/DocumentList'; // Placeholder for now
import SearchBar from '../SearchBar/SearchBar';
import { useUser } from '../Auth/UserContext';
const Dashboard = ({documents, onAddNewDocument}) => {
  const { user } = useUser();
//console.log(documents)
const handleNewDocument = (newDoc) => {
  onAddNewDocument(newDoc); 

};

  return (
    <div>
      <h2>Dashboard</h2>
      <DocumentUploader onNewDocument={handleNewDocument} />
      <DocumentList documents={documents} />
    </div>
  );
};

export default Dashboard;
