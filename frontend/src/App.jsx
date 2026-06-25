import { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL ||
  (window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000'
    : `http://${window.location.hostname}:8000`);

function App() {
  const [issue, setIssue] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch(`${API_BASE_URL}/report-issue`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ description: issue }),
    });

    const data = await response.json();
    setResult(JSON.stringify(data, null, 2));
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>BSNL AI Agent</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={issue}
          onChange={(e) => setIssue(e.target.value)}
          rows="5"
          cols="60"
          placeholder="Describe the issue..."
        />
        <br /><br />
        <button type="submit">Submit</button>
      </form>

      <h3>Result</h3>
      <pre>{result}</pre>
    </div>
  );
}

export default App;