import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = ({ onSearchResult }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sentiment, setSentiment] = useState('');
  const [filter, setFilter] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5000/search', {
        searchTerm,
        sentiment,
        filter,
      });
      // Assuming the response contains an array of documents or excerpts
      onSearchResult(response.data);
    } catch (error) {
      console.error('Search failed:', error);
      // Handle error (e.g., display an error message)
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <select value={sentiment} onChange={(e) => setSentiment(e.target.value)}>
        <option value="">Any Sentiment</option>
        <option value="positive">Positive</option>
        <option value="neutral">Neutral</option>
        <option value="negative">Negative</option>
      </select>
      <select value={filter} onChange={(e) => setFilter(e.target.value)}>
        <option value="">All</option>
        <option value="sentences">Sentences</option>
        <option value="paragraphs">Paragraphs</option>
      </select>
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchBar;
