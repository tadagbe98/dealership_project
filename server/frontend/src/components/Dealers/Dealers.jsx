import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const US_STATES = [
  'All', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
  'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois',
  'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
  'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
  'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
  'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
  'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
];

function Dealers({ isLoggedIn, userName }) {
  const [dealers, setDealers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedState, setSelectedState] = useState('All');
  const [search, setSearch] = useState('');

  const fetchDealers = async (state = 'All') => {
    setLoading(true);
    try {
      let url = '/djangoapp/get_dealers';
      if (state !== 'All') {
        url = `/djangoapp/get_dealers/${state}`;
      }
      const res = await fetch(url);
      const data = await res.json();
      setDealers(data.dealers || []);
    } catch (err) {
      console.error('Error fetching dealers:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDealers();
  }, []);

  const handleStateChange = (e) => {
    const state = e.target.value;
    setSelectedState(state);
    fetchDealers(state);
  };

  const filteredDealers = dealers.filter(d =>
    d.full_name?.toLowerCase().includes(search.toLowerCase()) ||
    d.city?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      {/* Hero */}
      <div className="page-hero">
        <h1>🚗 Car Dealerships</h1>
        <p>Find trusted dealerships across the United States</p>
      </div>

      {/* Filters */}
      <div style={{ background: 'white', padding: '20px 30px', borderBottom: '1px solid #eee', display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center' }}>
        <div style={{ flex: 1, minWidth: '200px' }}>
          <input
            type="text"
            className="form-control"
            placeholder="🔍 Search by name or city..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div>
          <select
            className="form-control"
            value={selectedState}
            onChange={handleStateChange}
            style={{ minWidth: '180px' }}
          >
            {US_STATES.map(st => (
              <option key={st} value={st}>{st === 'All' ? 'All States' : st}</option>
            ))}
          </select>
        </div>
        {isLoggedIn && (
          <div style={{ color: '#1a3c6e', fontWeight: 600, fontSize: '0.95rem' }}>
            ✅ Logged in as: <strong>{userName}</strong>
          </div>
        )}
      </div>

      {/* Dealer Grid */}
      <div style={{ padding: '30px', maxWidth: '1200px', margin: '0 auto' }}>
        {loading ? (
          <div className="spinner"></div>
        ) : filteredDealers.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '60px', color: '#666' }}>
            <div style={{ fontSize: '3rem', marginBottom: '16px' }}>🔍</div>
            <h3>No dealers found</h3>
            <p>Try adjusting your search or state filter</p>
          </div>
        ) : (
          <div className="row">
            {filteredDealers.map((dealer, idx) => (
              <div key={dealer.id || idx} className="col-3">
                <div className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                    <span style={{ background: '#1a3c6e', color: 'white', padding: '4px 10px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 600 }}>
                      ID: {dealer.id}
                    </span>
                    <span style={{ background: '#f0f4f8', color: '#1a3c6e', padding: '4px 10px', borderRadius: '20px', fontSize: '0.8rem' }}>
                      {dealer.st}
                    </span>
                  </div>

                  <h3 style={{ color: '#1a3c6e', fontWeight: 700, marginBottom: '8px', fontSize: '1.1rem' }}>
                    {dealer.full_name}
                  </h3>

                  <p style={{ color: '#666', fontSize: '0.9rem', marginBottom: '6px' }}>
                    📍 {dealer.city}, {dealer.state}
                  </p>
                  <p style={{ color: '#888', fontSize: '0.85rem', marginBottom: '16px' }}>
                    {dealer.address}, {dealer.zip}
                  </p>

                  <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                    <Link
                      to={`/dealer/${dealer.id}`}
                      className="btn btn-primary"
                      style={{ flex: 1, textAlign: 'center', fontSize: '0.85rem', padding: '8px 12px' }}
                    >
                      View Reviews
                    </Link>
                    {isLoggedIn && (
                      <Link
                        to={`/postreview/${dealer.id}`}
                        className="btn btn-danger"
                        style={{ flex: 1, textAlign: 'center', fontSize: '0.85rem', padding: '8px 12px' }}
                      >
                        Review Dealer
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <footer>
        <p><strong>🚗 Best Cars Dealership</strong> &copy; 2024. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Dealers;
