import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function Dealer({ isLoggedIn, userName }) {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dealerRes, reviewsRes] = await Promise.all([
          fetch(`/djangoapp/dealer/${id}`),
          fetch(`/djangoapp/reviews/dealer/${id}`)
        ]);
        const dealerData = await dealerRes.json();
        const reviewsData = await reviewsRes.json();
        setDealer(dealerData.dealer || null);
        setReviews(reviewsData.reviews || []);
      } catch (err) {
        console.error('Error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const getSentimentBadge = (sentiment) => {
    if (!sentiment) return null;
    const classes = {
      positive: 'badge-positive',
      negative: 'badge-negative',
      neutral: 'badge-neutral',
    };
    const icons = { positive: '😊', negative: '😞', neutral: '😐' };
    return (
      <span className={classes[sentiment] || 'badge-neutral'}>
        {icons[sentiment] || '😐'} {sentiment}
      </span>
    );
  };

  if (loading) return <div className="spinner"></div>;

  return (
    <div>
      {/* Dealer Header */}
      <div className="page-hero">
        {dealer ? (
          <>
            <h1>{dealer.full_name}</h1>
            <p>📍 {dealer.city}, {dealer.state} — {dealer.address}</p>
          </>
        ) : (
          <h1>Dealer #{id}</h1>
        )}
      </div>

      <div style={{ maxWidth: '900px', margin: '30px auto', padding: '0 20px' }}>
        {/* Action Buttons */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
          <Link to="/" className="btn btn-outline">← All Dealers</Link>
          {isLoggedIn ? (
            <Link to={`/postreview/${id}`} className="btn btn-danger">
              ✍️ Write a Review
            </Link>
          ) : (
            <div style={{ color: '#666', fontSize: '0.9rem' }}>
              <Link to="/login" style={{ color: '#1a3c6e', fontWeight: 600 }}>Login</Link> to post a review
            </div>
          )}
        </div>

        {/* Dealer Info Card */}
        {dealer && (
          <div className="card" style={{ marginBottom: '24px' }}>
            <h3 style={{ color: '#1a3c6e', marginBottom: '12px' }}>Dealer Information</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div><strong>Full Name:</strong> {dealer.full_name}</div>
              <div><strong>Short Name:</strong> {dealer.short_name}</div>
              <div><strong>City:</strong> {dealer.city}</div>
              <div><strong>State:</strong> {dealer.state} ({dealer.st})</div>
              <div><strong>Address:</strong> {dealer.address}</div>
              <div><strong>Zip Code:</strong> {dealer.zip}</div>
            </div>
          </div>
        )}

        {/* Reviews Section */}
        <h2 style={{ color: '#1a3c6e', marginBottom: '16px' }}>
          Customer Reviews ({reviews.length})
        </h2>

        {reviews.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '12px' }}>💬</div>
            <h4>No reviews yet</h4>
            <p>Be the first to review this dealership!</p>
            {isLoggedIn && (
              <Link to={`/postreview/${id}`} className="btn btn-primary" style={{ marginTop: '16px' }}>
                Write First Review
              </Link>
            )}
          </div>
        ) : (
          reviews.map((review, idx) => (
            <div key={review.id || idx} className="card" style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px', flexWrap: 'wrap', gap: '8px' }}>
                <div>
                  <strong style={{ fontSize: '1rem', color: '#1a3c6e' }}>{review.name}</strong>
                  {review.purchase && (
                    <span style={{ marginLeft: '10px', background: '#d4edda', color: '#155724', padding: '2px 10px', borderRadius: '12px', fontSize: '0.8rem' }}>
                      ✅ Verified Purchase
                    </span>
                  )}
                </div>
                {getSentimentBadge(review.sentiment)}
              </div>

              <p style={{ color: '#333', lineHeight: 1.6, marginBottom: '10px' }}>
                "{review.review}"
              </p>

              {(review.car_make || review.car_model || review.car_year) && (
                <div style={{ background: '#f8f9fa', padding: '8px 14px', borderRadius: '8px', fontSize: '0.85rem', color: '#555' }}>
                  🚗 {review.car_year} {review.car_make} {review.car_model}
                  {review.purchase_date && ` — Purchased: ${review.purchase_date}`}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      <footer>
        <p><strong>🚗 Best Cars Dealership</strong> &copy; 2024. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Dealer;
