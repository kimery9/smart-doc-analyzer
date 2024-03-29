import React, { useState } from 'react';
import axios from 'axios';
import DocumentSummary from '../DocumentSummary/DocumentSummary';
import KeywordList from '../KeywordList/KeywordList';
import KeywordArticles from '../Dashboard/KeywordArticles';
import { Button, Input, Select, List, Typography, Divider } from 'antd';
const { Option } = Select;


const DocumentList = ({ documents }) => {
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [summary, setSummary] = useState('');
  const [keywords, setKeywords] = useState([]);
  const [error, setError] = useState('');
const [searchKeyword, setSearchKeyword] = useState('');
const [filteredSentences, setFilteredSentences] = useState([]);
const [filteredParagraphs, setFilteredParagraphs] = useState([]);


  const fetchSummary = async (filename) => {
    try {
        console.log(filename)
      const response = await axios.post('http://localhost:5000/document/summary', { filename });
      setSummary(response.data.summary);
      setSelectedDoc(filename);
      // Clear previous keywords and errors
      setKeywords([]);
      setError('');
    } catch (err) {
      setSummary('Failed to fetch summary. ChatGPT quota reached');
      setKeywords([]);
      alert('Failed to fetch summary. ChatGPT quota reached');
    }
  };

  const fetchKeywords = async (filename) => {
    try {
        const response = await axios.post('http://localhost:5000/document/keywords', { filename: filename });
        if (response.data.keywords) {
            setKeywords(response.data.keywords);
            setSelectedDoc(filename);
            setError('');
        } else {
            setError('No keywords found for this document.');
        }
    } catch (err) {
        setError('Failed to fetch keywords.ChatGPT quota reached');
        console.error(err);
    }
};

const fetchFilteredBySentiment = async (sentiment) => {
  try {
    const response = await axios.get(`http://localhost:5000/api/filter/sentiment/${sentiment}`);
    setFilteredSentences(response.data.sentences);
    setFilteredParagraphs(response.data.paragraphs);
    // Resetting other states as necessary
    setSummary('');
    setKeywords([]);
    setError('');
  } catch (err) {
    console.error('Failed to fetch filtered data', err);
    setError('Failed to fetch filtered data. Please try again later.');
  }
};

const fetchByKeyword = async (keyword) => {
  try {
    const response = await axios.post('http://localhost:5000/api/search/keyword', { keyword });
    setFilteredSentences(response.data.sentences);
    setFilteredParagraphs(response.data.paragraphs);
    // Resetting other states as necessary
    setSummary('');
    setKeywords([]);
    setError('');
  } catch (err) {
    console.error('Failed to fetch by keyword', err);
    setError('Failed to search by keyword. Please try again later.');
  }
};


return (
  <div style={{ padding: '20px' }}>
    <Typography.Title level={3}>Uploaded Documents</Typography.Title>
    {error && <p className="error">{error}</p>}

    <div style={{ marginBottom: '20px' }}>
      <Input
        style={{ width: '200px', marginRight: '10px' }}
        value={searchKeyword}
        onChange={(e) => setSearchKeyword(e.target.value)}
        placeholder="Enter keyword"
      />
      <Button type="primary" onClick={() => fetchByKeyword(searchKeyword)}>Search</Button>
    </div>

    <div style={{ marginBottom: '20px' }}>
    <Select
      style={{ width: '200px' }}
      onChange={(value) => {
        console.log('Selected Sentiment:', value); // Sanity check logging
        fetchFilteredBySentiment(value);
      }}
      placeholder="Filter by Sentiment"
      allowClear
    >
      <Option value="positive">Positive</Option>
      <Option value="negative">Negative</Option>
      <Option value="neutral">Neutral</Option>
    </Select>

    </div>

    <List
      bordered
      dataSource={documents}
      renderItem={(doc, index) => (
        <List.Item key={index}>
          <Typography.Text>{doc.filename} - Sentiment: {doc.sentiment}</Typography.Text>
          <div>
            <Button type="link" onClick={() => fetchSummary(doc.filename)}>Get Summary</Button>
            <Button type="link" onClick={() => fetchKeywords(doc.filename)}>Show Keywords</Button>
            {selectedDoc === doc.filename && (
              <>
                <DocumentSummary summary={summary} filename={selectedDoc} />
                <KeywordList keywords={keywords} filename={selectedDoc} />
                <KeywordArticles keywords={keywords} />
              </>
            )}
          </div>
        </List.Item>
      )}
    />

    {filteredSentences.length > 0 && (
      <>
        <Divider />
        <Typography.Title level={4}>Filtered Sentences</Typography.Title>
        {filteredSentences.map((sentence, index) => (
          <p key={index}>{sentence.content}</p>
        ))}
      </>
    )}

    {filteredParagraphs.length > 0 && (
      <>
        <Divider />
        <Typography.Title level={4}>Filtered Paragraphs</Typography.Title>
        {filteredParagraphs.map((paragraph, index) => (
          <p key={index}>{paragraph.content}</p>
        ))}
      </>
    )}
  </div>
);

      }

export default DocumentList;
