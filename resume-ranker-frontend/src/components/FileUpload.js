import React, { useRef } from 'react';
import './FileUpload.css';
import axios from 'axios';



function FileUpload({ onFileChange }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    onFileChange(e.target.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileChange(e.dataTransfer.files);
      e.dataTransfer.clearData();
    }
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Resumes</h2>
      <div 
        className="drop-area"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <p>Drag and drop resume files here, or click to select files</p>
        <p className="file-format">(Accepted formats: PDF, TXT)</p>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.txt"
          multiple
          style={{ display: 'none' }}
        />
      </div>
     
    </div>
  );
}

export default FileUpload;
