import React, { useState } from 'react';
import axios from 'axios';
import { List, Button, Tooltip } from 'antd';

const KeywordList = ({ keywords, filename }) => {
  const [definitions, setDefinitions] = useState({});
  const [err, setError]=useState()

  const fetchKeywordDefinition = async (keyword) => {
    if (definitions[keyword]) {
      return; // Avoid refetching
    }
    try {
      const response = await axios.post('http://localhost:5000/keyword/definition', { keyword });
      setDefinitions({
        ...definitions,
        [keyword]: response.data.definition,
      });
    } catch (error) {
      setError(`Failed to fetch definition for ${keyword} due to insufficient ChatGPT quota.`);
    }
  };

  return (
    <div>
      <h4>Keywords for {filename}</h4>
      {err && <p className="error">{err}</p>}
      <List
        dataSource={keywords}
        renderItem={(keyword) => (
          <List.Item>
            <Tooltip title={definitions[keyword] || 'Click to get definition'}>
              <Button type="link" onClick={() => fetchKeywordDefinition(keyword)}>
                {keyword}
              </Button>
            </Tooltip>
          </List.Item>
        )}
      />
    </div>
  );
};

export default KeywordList;
