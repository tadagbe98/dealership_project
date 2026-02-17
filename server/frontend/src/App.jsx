import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import Dealers from './components/Dealers/Dealers';
import Dealer from './components/Dealer/Dealer';
import PostReview from './components/PostReview/PostReview';
import Login from './components/Login/Login';
import Register from './components/Register/Register';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');
  const [firstName, setFirstName] = useState('');

  useEffect(() => {
    const savedUser = sessionStorage.getItem('username');
    const savedFirstName = sessionStorage.getItem('firstname');
    if (savedUser) {
      setIsLoggedIn(true);
      setUserName(savedUser);
      setFirstName(savedFirstName || '');
    }
  }, []);

  const handleLogin = (username, first) => {
    setIsLoggedIn(true);
    setUserName(username);
    setFirstName(first || '');
    sessionStorage.setItem('username', username);
    sessionStorage.setItem('firstname', first || '');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserName('');
    setFirstName('');
    sessionStorage.removeItem('username');
    sessionStorage.removeItem('firstname');
    fetch('/djangoapp/logout', { method: 'GET', credentials: 'include' });
  };

  return (
    <Router>
      <Header
        isLoggedIn={isLoggedIn}
        userName={userName}
        firstName={firstName}
        onLogout={handleLogout}
      />
      <Routes>
        <Route path="/" element={<Dealers isLoggedIn={isLoggedIn} userName={userName} />} />
        <Route path="/dealers" element={<Dealers isLoggedIn={isLoggedIn} userName={userName} />} />
        <Route path="/dealer/:id" element={<Dealer isLoggedIn={isLoggedIn} userName={userName} />} />
        <Route path="/postreview/:id" element={<PostReview isLoggedIn={isLoggedIn} userName={userName} />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register onLogin={handleLogin} />} />
      </Routes>
    </Router>
  );
}

export default App;
