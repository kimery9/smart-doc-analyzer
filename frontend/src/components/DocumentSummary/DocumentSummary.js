import React from 'react';
import { Typography, Card } from 'antd';

const { Title, Paragraph } = Typography;

const DocumentSummary = ({ summary, filename }) => {
  return (
    <Card bordered style={{ marginTop: 16 }}>
      <Title level={4}>Summary for {filename}</Title>
      <Paragraph>{summary}</Paragraph>
    </Card>
  );
};

export default DocumentSummary;
