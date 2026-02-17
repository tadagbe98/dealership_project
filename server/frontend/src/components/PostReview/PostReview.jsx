import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';

function PostReview({ isLoggedIn, userName }) {
  const { id } = useParams();
  const navigate = useNavigate();

  const [dealer, setDealer] = useState(null);
  const [carMakes, setCarMakes] = useState([]);
  const [carModels, setCarModels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const [formData, setFormData] = useState({
    review: '',
    purchase: false,
    purchase_date: '',
    car_make: '',
    car_model: '',
    car_year: new Date().getFullYear(),
  });

  useEffect(() => {
    if (!isLoggedIn) {
      navigate('/login');
      return;
    }

    const fetchData = async () => {
      try {
        const [dealerRes, carsRes] = await Promise.all([
          fetch(`/djangoapp/dealer/${id}`),
          fetch('/djangoapp/get_cars')
        ]);
        const dealerData = await dealerRes.json();
        const carsData = await carsRes.json();
        setDealer(dealerData.dealer || null);

        const makes = [...new Set((carsData.CarModels || []).map(c => c.CarMake))];
        setCarMakes(makes);
        setCarModels(carsData.CarModels || []);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, [id, isLoggedIn]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({ ...formData, [name]: type === 'checkbox' ? checked : value });
  };

  const filteredModels = carModels.filter(cm => cm.CarMake === formData.car_make);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = {
        ...formData,
        dealership: parseInt(id),
        userName,
      };

      const res = await fetch('/djangoapp/add_review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (data.status === 200) {
        setSubmitted(true);
        setTimeout(() => navigate(`/dealer/${id}`), 2000);
      }
    } catch (err) {
      console.error('Error submitting review:', err);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div style={{ textAlign: 'center', padding: '80px', color: '#1a3c6e' }}>
        <div style={{ fontSize: '4rem', marginBottom: '20px' }}>✅</div>
        <h2>Review Submitted!</h2>
        <p style={{ color: '#666', marginTop: '10px' }}>Redirecting to dealer page...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-hero">
        <h1>✍️ Post a Review</h1>
        <p>{dealer ? dealer.full_name : `Dealer #${id}`}</p>
      </div>

      <div style={{ maxWidth: '700px', margin: '30px auto', padding: '0 20px' }}>
        <div style={{ marginBottom: '20px' }}>
          <Link to={`/dealer/${id}`} className="btn btn-outline">← Back to Dealer</Link>
        </div>

        <div className="card">
          <h3 style={{ color: '#1a3c6e', marginBottom: '24px' }}>Share Your Experience</h3>
          <p style={{ color: '#666', marginBottom: '24px', fontSize: '0.9rem' }}>
            Posting as: <strong>{userName}</strong>
          </p>

          <form onSubmit={handleSubmit}>
            {/* Review Text */}
            <div className="form-group">
              <label className="form-label">Your Review *</label>
              <textarea
                name="review"
                className="form-control"
                rows={5}
                placeholder="Share your experience with this dealership..."
                value={formData.review}
                onChange={handleChange}
                required
                style={{ resize: 'vertical' }}
              />
            </div>

            {/* Purchase checkbox */}
            <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <input
                type="checkbox"
                name="purchase"
                id="purchase"
                checked={formData.purchase}
                onChange={handleChange}
                style={{ width: '18px', height: '18px', cursor: 'pointer' }}
              />
              <label htmlFor="purchase" style={{ cursor: 'pointer', fontWeight: 600 }}>
                I purchased a car from this dealership
              </label>
            </div>

            {/* Purchase Date - shown if purchased */}
            {formData.purchase && (
              <div className="form-group">
                <label className="form-label">Purchase Date</label>
                <input
                  type="date"
                  name="purchase_date"
                  className="form-control"
                  value={formData.purchase_date}
                  onChange={handleChange}
                />
              </div>
            )}

            {/* Car Make */}
            <div className="form-group">
              <label className="form-label">Car Make</label>
              <select
                name="car_make"
                className="form-control"
                value={formData.car_make}
                onChange={handleChange}
              >
                <option value="">-- Select Car Make --</option>
                {carMakes.map(make => (
                  <option key={make} value={make}>{make}</option>
                ))}
              </select>
            </div>

            {/* Car Model */}
            <div className="form-group">
              <label className="form-label">Car Model</label>
              <select
                name="car_model"
                className="form-control"
                value={formData.car_model}
                onChange={handleChange}
                disabled={!formData.car_make}
              >
                <option value="">-- Select Car Model --</option>
                {filteredModels.map((cm, i) => (
                  <option key={i} value={cm.CarModel}>{cm.CarModel} ({cm.CarType})</option>
                ))}
              </select>
            </div>

            {/* Car Year */}
            <div className="form-group">
              <label className="form-label">Car Year</label>
              <select
                name="car_year"
                className="form-control"
                value={formData.car_year}
                onChange={handleChange}
              >
                {[2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015].map(yr => (
                  <option key={yr} value={yr}>{yr}</option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              style={{ width: '100%', padding: '14px', fontSize: '1rem', marginTop: '8px' }}
              disabled={loading}
            >
              {loading ? '⏳ Submitting...' : '🚀 Submit Review'}
            </button>
          </form>
        </div>
      </div>

      <footer>
        <p><strong>🚗 Best Cars Dealership</strong> &copy; 2024. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default PostReview;
