import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import JobDescription from './components/JobDescription';
import Results from './components/Results';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleJobDescriptionChange = (text) => {
    setJobDescription(text);
  };

  const handleFileChange = (files) => {
    setSelectedFiles(files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!jobDescription) {
      setError('Please enter a job description');
      return;
    }
    
    if (selectedFiles.length === 0) {
      setError('Please upload at least one resume');
      return;
    }
    
    setError('');
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('jobDescription', jobDescription);
      
      for (let i = 0; i < selectedFiles.length; i++) {
        formData.append('resumes', selectedFiles[i]);
      }
      
      const response = await fetch('http://localhost:8000/api/rank-resumes/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Something went wrong with the request');
      }
      
      const data = await response.json();
      setRankings(data.rankings);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Resume Ranker</h1>
        <p>Upload resumes and enter a job description to find the best matches</p>
      </header>
      <main className="app-content">
        <form onSubmit={handleSubmit}>
          <div className="input-section">
            <FileUpload onFileChange={handleFileChange} />
            <JobDescription onDescriptionChange={handleJobDescriptionChange} />
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Processing...' : 'Rank Resumes'}
          </button>
        </form>
        
        {rankings.length > 0 && <Results rankings={rankings} />}
      </main>
    </div>
  );
}

export default App;