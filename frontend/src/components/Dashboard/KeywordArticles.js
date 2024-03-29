import React, { useState } from 'react';
import axios from 'axios';
import { Typography, List, Button, Alert } from 'antd';
import { useUser } from '../Auth/UserContext';

const { Title, Link } = Typography;

const KeywordArticles = ({ keywords }) => {
  const [selectedKeyword, setSelectedKeyword] = useState('');
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState('');

  const fetchArticles = async (keyword) => {
    try {
      const response = await axios.post('http://localhost:5000/search', { keyword });
      setArticles(response.data.links);
      setSelectedKeyword(keyword);
      setError('');
    } catch (err) {
      console.error('Failed to fetch articles', err);
      setError('Failed to fetch articles. Please try again later.');
      setArticles([]); // Clear previous articles on error
    }
  };

  return (
    <div>
      <Title level={4}>More articles about:</Title>
      {keywords.map((keyword, index) => (
        <Button key={index} type="primary" onClick={() => fetchArticles(keyword)} style={{ margin: '5px' }}>
          {keyword}
        </Button>
      ))}
      
      {selectedKeyword && (
        <>
          <Title level={4}>Articles for "{selectedKeyword}"</Title>
          <List
            dataSource={articles}
            renderItem={(article, index) => (
              <List.Item key={index}>
                <Link href={article} target="_blank">
                  {article}
                </Link>
              </List.Item>
            )}
          />
          {articles.length === 0 && <p>No articles found.</p>}
        </>
      )}

      {error && <Alert message={error} type="error" showIcon />}
    </div>
  );
};

export default KeywordArticles;
