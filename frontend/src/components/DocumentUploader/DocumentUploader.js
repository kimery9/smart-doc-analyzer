import React, { useState } from 'react';
import { useUser } from '../Auth/UserContext';
import { Upload, Button, Spin, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const DocumentUploader = ({ onNewDocument }) => {
  const [fileList, setFileList] = useState([]);
  const [uploading, setUploading] = useState(false);
  const { user } = useUser();

  const beforeUpload = (file) => {
    setFileList([...fileList, file]);
    // Prevent automatic upload
    return false;
  };

  const handleUpload = async () => {
    if (fileList.length === 0) {
      message.error("Please select one or more files.");
      return;
    }
    if (!user || !user.sub) {
      message.error('No valid user ID found. Please log in again.');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    fileList.forEach((file) => {
      formData.append('file', file);
    });
    formData.append('userId', user.sub);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: 'POST',
        body: formData,
      });

      setUploading(false);

      if (response.ok) {
        const data = await response.json();
        console.log(data)
        onNewDocument(data);
        message.success("Files uploaded successfully.");
        setFileList([]); // Clear the list after upload
      } else {
        const errorData = await response.json();
        message.error(errorData.error || 'File upload failed');
      }
    } catch (error) {
      console.error('Error uploading files:', error);
      message.error(error.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <Spin spinning={uploading}>
      <Upload
        beforeUpload={beforeUpload}
        onRemove={(file) => setFileList(fileList.filter(item => item.uid !== file.uid))}
        fileList={fileList}
        multiple
      >
        <Button icon={<UploadOutlined />}>Select Files</Button>
      </Upload>
      <Button
        type="primary"
        onClick={handleUpload}
        disabled={uploading || fileList.length === 0}
        style={{ marginTop: 16 }}
      >
        {uploading ? 'Uploading' : 'Start Upload'}
      </Button>
    </Spin>
  );
};

export default DocumentUploader;
