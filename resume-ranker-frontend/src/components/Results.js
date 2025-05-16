import React from 'react';
import './Results.css'; // Assuming the styles are now in an external CSS file.

function Results({ rankings }) {
  return (
    <div className="results-container">
      <h2>Resume Rankings</h2>
      <div className="results-list">
        {rankings.map((resume, index) => (
          <div 
            key={index} 
            className="result-item"
            style={{
              borderLeft: `5px solid ${getColorByPercentage(resume.match_percentage)}`
            }}
          >
            <div className="result-content">
              <h3>{resume.name}</h3>
              <div className="match-container">
                <div className="match-bar">
                  <div 
                    className="match-fill" 
                    style={{ 
                      width: `${resume.match_percentage}%`,
                      backgroundColor: getColorByPercentage(resume.match_percentage)
                    }}
                  ></div>
                </div>
                <span className="match-percentage">{resume.match_percentage}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function getColorByPercentage(percentage) {
  if (percentage >= 80) {
    return '#27ae60'; // Green (high match)
  } else if (percentage >= 60) {
    return '#2ecc71'; // Light green (good match)
  } else if (percentage >= 40) {
    return '#f39c12'; // Orange (moderate match)
  } else if (percentage >= 20) {
    return '#e67e22'; // Dark orange (low match)
  } else {
    return '#e74c3c'; // Red (very low match)
  }
}

export default Results;
