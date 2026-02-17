import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Register({ onLogin }) {
  const [formData, setFormData] = useState({
    userName: '',
    firstName: '',
    lastName: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/djangoapp/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.error === 'Already Registered') {
        setError('This username is already taken. Please choose a different one.');
      } else if (data.status === 'Authenticated') {
        onLogin(data.userName, data.firstName);
        navigate('/');
      } else {
        setError('Registration failed. Please try again.');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f5f5f5', padding: '40px 20px' }}>
      <div style={{ background: 'white', borderRadius: '16px', padding: '48px', width: '100%', maxWidth: '480px', boxShadow: '0 8px 32px rgba(0,0,0,0.12)' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{ fontSize: '3rem', marginBottom: '10px' }}>🚗</div>
          <h2 style={{ color: '#1a3c6e', fontWeight: 700 }}>Create Account</h2>
          <p style={{ color: '#666', marginTop: '8px' }}>Join the Best Cars community</p>
        </div>

        {error && (
          <div style={{ background: '#f8d7da', color: '#721c24', padding: '12px', borderRadius: '8px', marginBottom: '20px', textAlign: 'center' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Username Field */}
          <div className="form-group">
            <label className="form-label">Username *</label>
            <input
              type="text"
              name="userName"
              className="form-control"
              placeholder="Choose a username"
              value={formData.userName}
              onChange={handleChange}
              required
            />
          </div>

          {/* First Name Field */}
          <div className="form-group">
            <label className="form-label">First Name *</label>
            <input
              type="text"
              name="firstName"
              className="form-control"
              placeholder="Enter your first name"
              value={formData.firstName}
              onChange={handleChange}
              required
            />
          </div>

          {/* Last Name Field */}
          <div className="form-group">
            <label className="form-label">Last Name *</label>
            <input
              type="text"
              name="lastName"
              className="form-control"
              placeholder="Enter your last name"
              value={formData.lastName}
              onChange={handleChange}
              required
            />
          </div>

          {/* Email Field */}
          <div className="form-group">
            <label className="form-label">Email Address *</label>
            <input
              type="email"
              name="email"
              className="form-control"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          {/* Password Field */}
          <div className="form-group">
            <label className="form-label">Password *</label>
            <input
              type="password"
              name="password"
              className="form-control"
              placeholder="Create a secure password"
              value={formData.password}
              onChange={handleChange}
              required
              minLength={6}
            />
          </div>

          {/* Register Button */}
          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '12px', fontSize: '1rem', marginTop: '8px' }}
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '24px', color: '#666' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: '#1a3c6e', fontWeight: 600 }}>
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
