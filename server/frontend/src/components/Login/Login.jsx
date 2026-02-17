import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Login({ onLogin }) {
  const [userName, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/djangoapp/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ userName, password }),
      });

      const data = await response.json();

      if (data.status === 'Authenticated') {
        onLogin(data.userName, data.firstName);
        navigate('/');
      } else {
        setError('Invalid username or password. Please try again.');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f5f5f5' }}>
      <div style={{ background: 'white', borderRadius: '16px', padding: '48px', width: '100%', maxWidth: '420px', boxShadow: '0 8px 32px rgba(0,0,0,0.12)' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{ fontSize: '3rem', marginBottom: '10px' }}>🚗</div>
          <h2 style={{ color: '#1a3c6e', fontWeight: 700 }}>Welcome Back</h2>
          <p style={{ color: '#666', marginTop: '8px' }}>Sign in to your account</p>
        </div>

        {error && (
          <div style={{ background: '#f8d7da', color: '#721c24', padding: '12px', borderRadius: '8px', marginBottom: '20px', textAlign: 'center' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter your username"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '12px', fontSize: '1rem', marginTop: '8px' }}
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '24px', color: '#666' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ color: '#1a3c6e', fontWeight: 600 }}>
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
