import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Header({ isLoggedIn, userName, firstName, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        🚗 Best Cars Dealership
      </Link>
      <ul className="navbar-nav">
        <li>
          <a className="nav-link" href="/static/About.html">About Us</a>
        </li>
        <li>
          <a className="nav-link" href="/static/Contact.html">Contact Us</a>
        </li>
        {isLoggedIn ? (
          <>
            <li>
              <span className="nav-link" style={{ color: '#ffd166', fontWeight: 700 }}>
                👤 {firstName || userName}
              </span>
            </li>
            <li>
              <button
                className="btn btn-danger"
                onClick={handleLogout}
                style={{ padding: '8px 18px', fontSize: '0.9rem' }}
              >
                Logout
              </button>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/login" className="btn btn-outline" style={{ color: 'white', borderColor: 'white' }}>
                Login
              </Link>
            </li>
            <li>
              <Link to="/register" className="btn btn-primary" style={{ background: '#e63946' }}>
                Register
              </Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Header;
