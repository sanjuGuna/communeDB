import React, { useState, useEffect, useRef } from 'react';

export default function App() {
  const [prompt, setPrompt] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [connection, setConnection] = useState({ host: '', port: '', user: '', password: '', database: '' });
  const scrollRef = useRef(null);

  const handleSubmit = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt before submitting.');
      return;
    }

    setLoading(true);
    setError('');
    setResponseData(null);

    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, connection })
      });
      const result = await res.json();
      if (result.error) {
        setError(result.error);
      } else {
        setResponseData(result);
      }
    } catch (err) {
      setError('Failed to connect to server: ' + err.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [responseData]);

  const handleClear = () => {
    setPrompt('');
    setResponseData(null);
    setError('');
  };

  const handleConnectionChange = (e) => {
    setConnection({ ...connection, [e.target.name]: e.target.value });
  };

  return (
    <div id="root">
      <div className="container">
        <h1>Communicate with Database</h1>

        <div className="input-group">
          {['host', 'port', 'user', 'password', 'database'].map((field) => (
            <input
              key={field}
              name={field}
              value={connection[field]}
              onChange={handleConnectionChange}
              placeholder={field.charAt(0).toUpperCase() + field.slice(1)}
              type={field === 'password' ? 'password' : 'text'}
            />
          ))}
        </div>

        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your SQL-related prompt here..."
        ></textarea>

        <div className="button-group">
          <button 
            className="primary" 
            onClick={handleSubmit} 
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="loading"></span>
                Generating...
              </>
            ) : 'Run Query'}
          </button>
          <button 
            className="secondary" 
            onClick={handleClear}
          >
            Clear
          </button>
        </div>

        {error && <p className="error-message">❌ {error}</p>}

        {responseData && (
          <div ref={scrollRef} className="sql-output">
            <h2>Generated SQL:</h2>
            <div className="code-block">
              {responseData.sql}
              <button 
                className="small copy-button"
                onClick={() => navigator.clipboard.writeText(responseData.sql)}
              >
                Copy
              </button>
            </div>

            <h2>Output:</h2>
            <table className="results-table">
              <thead>
                <tr>
                  {Object.keys(responseData.data[0] || {}).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {responseData.data.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {Object.values(row).map((value, colIndex) => (
                      <td key={colIndex}>{value}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}