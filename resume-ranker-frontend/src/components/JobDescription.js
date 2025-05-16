import React, { useState } from 'react';

function JobDescription({ onDescriptionChange }) {
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const value = e.target.value;
    onDescriptionChange(value);
    if (!value.trim()) {
      setError('Job description cannot be empty.');
    } else {
      setError('');
    }
  };

  return (
    <div className="job-description-container">
      <h2>Job Description</h2>
      <textarea
        className="job-description-input"
        placeholder="Paste the job description here..."
        onChange={handleChange}
        rows={8}
      ></textarea>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default JobDescription;
