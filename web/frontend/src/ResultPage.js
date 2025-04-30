import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './style.css';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { result, formData } = location.state || {};

  if (!result) {
    navigate('/');
    return null;
  }

  return (
    <div className="container">
      <div className="card">
        <h2 className="heading">🩺 Prediction Results</h2>
        <p className="description">Below are the predicted probabilities for each health condition, provided for your reference only:</p>
        <ul>
          {Object.entries(result.predictions).map(([disease, probability]) => (
            <li key={disease}>
              <strong>{disease}:</strong> {`${(probability * 100).toFixed(2)}%`}
            </li>
          ))}
        </ul>
        {result.advices && (
          <div className="advice-section">
            <h3>Recommendations</h3>
            <ReactMarkdown>{result.advices}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultPage;
