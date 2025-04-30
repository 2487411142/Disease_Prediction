import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HealthAssessmentForm from './HealthAssessmentForm';
import ResultPage from './ResultPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HealthAssessmentForm />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

