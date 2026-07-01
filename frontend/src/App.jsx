import { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL ||
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000'
    : 'https://bsnl-ai-agent-backend.onrender.com');

const exampleIssues = [
  'My internet is down and the router is not working',
  'Fiber line is cut in my area and the connection is offline',
  'Mobile signal is weak and I cannot make calls',
  'I need help with my recharge payment and billing issue',
];

function App() {
  const [issue, setIssue] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCallNow = (phone) => {
    window.location.href = `tel:${phone}`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!issue.trim()) {
      setResult({
        message: 'Please enter a problem description',
        category: 'Invalid',
        department: 'Unknown',
        priority: 'Low',
        assigned_to: 'No team',
        contact_number: '',
        description: '',
      });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/report-issue`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: issue }),
      });

      const contentType = response.headers.get('content-type') || '';
      const data = contentType.includes('application/json')
        ? await response.json()
        : await response.text();

      if (!response.ok) {
        throw new Error(typeof data === 'string' ? data : JSON.stringify(data));
      }

      setResult(data);
      if (data.contact_number) {
        window.location.href = `tel:${data.contact_number}`;
      }
    } catch (error) {
      setResult({
        message: `Error: ${error.message}`,
        category: 'Invalid',
        priority: 'Low',
        assigned_to: 'No team',
        description: issue,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="hero-card">
        <div className="hero-badge">⚡ BSNL AI Support</div>
        <h1>Describe your issue and get a guided response.</h1>
        <p className="subtext">
          Report problems like internet downtime, fiber cuts, mobile signal issues, or billing concerns.
          The assistant will classify the issue and suggest the right team.
        </p>

        <div className="hero-highlights">
          <span>Auto-routing</span>
          <span>Priority detection</span>
          <span>Fast support flow</span>
        </div>
      </div>

      <form className="issue-form" onSubmit={handleSubmit}>
        <label htmlFor="issue">What’s happening?</label>
        <textarea
          id="issue"
          value={issue}
          onChange={(e) => setIssue(e.target.value)}
          rows="6"
          placeholder="Example: My fiber connection is down and the internet is not working."
        />

        <div className="example-chips">
          {exampleIssues.map((example) => (
            <button type="button" key={example} className="chip" onClick={() => setIssue(example)}>
              {example}
            </button>
          ))}
        </div>

        <div className="form-actions">
          <button type="submit" disabled={loading}>
            {loading ? 'Checking issue...' : 'Submit issue'}
          </button>
          <p className="helper-text">Try words like network, fiber, mobile, bill, drop, or signal.</p>
        </div>
      </form>

      {result && (
        <div className={`result-card ${result.category === 'Invalid' ? 'invalid' : 'success'}`}>
          <div className="result-header">
            <span className="badge">{result.category || 'Result'}</span>
            <span className="priority">{result.priority || '—'}</span>
          </div>
          <h3>{result.message || 'Issue received'}</h3>
          <p className="result-description">
            <strong>Issue:</strong> {result.description || issue}
          </p>
          <p>
            <strong>Department:</strong> {result.department || 'Unknown'}
          </p>
          <p>
            <strong>Assigned to:</strong> {result.assigned_to || 'No team'}
          </p>
          <p>
            <strong>Contact:</strong>{' '}
            {result.contact_number ? (
              <a className="contact-link" href={`tel:${result.contact_number}`}>{result.contact_number}</a>
            ) : (
              'Not available yet'
            )}
          </p>
          {result.contact_number && (
            <button
              type="button"
              className="call-button"
              onClick={() => handleCallNow(result.contact_number)}
            >
              Call now
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default App;