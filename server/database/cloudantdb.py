"""
Database helper functions for IBM Cloudant NoSQL DB.
Handles CRUD operations for dealers and reviews.
"""

import os
import json
import requests
import logging

logger = logging.getLogger(__name__)

CLOUDANT_URL = os.environ.get("CLOUDANT_URL", "")
CLOUDANT_KEY = os.environ.get("CLOUDANT_KEY", "")
DEALERS_DB = "dealerships"
REVIEWS_DB = "reviews"


def get_database_client():
    """Get a Cloudant client instance."""
    if not CLOUDANT_URL or not CLOUDANT_KEY:
        logger.warning("Cloudant credentials not set. Using mock data.")
        return None
    
    try:
        from cloudant.client import Cloudant
        client = Cloudant.iam(
            None,
            CLOUDANT_KEY,
            url=CLOUDANT_URL,
            connect=True
        )
        return client
    except ImportError:
        logger.error("cloudant package not installed")
        return None
    except Exception as e:
        logger.error(f"Cloudant connection error: {e}")
        return None


def get_all_dealers():
    """Retrieve all dealers from Cloudant."""
    client = get_database_client()
    if not client:
        return _mock_dealers()
    
    try:
        db = client[DEALERS_DB]
        dealers = [doc for doc in db]
        client.disconnect()
        return dealers
    except Exception as e:
        logger.error(f"Error fetching dealers: {e}")
        return _mock_dealers()


def get_dealers_by_state(state):
    """Retrieve dealers filtered by state."""
    all_dealers = get_all_dealers()
    return [d for d in all_dealers if d.get("state", "").lower() == state.lower()]


def get_dealer_by_id(dealer_id):
    """Retrieve a single dealer by ID."""
    all_dealers = get_all_dealers()
    for dealer in all_dealers:
        if str(dealer.get("id", "")) == str(dealer_id):
            return dealer
    return None


def get_reviews_for_dealer(dealer_id):
    """Retrieve all reviews for a specific dealer."""
    client = get_database_client()
    if not client:
        return _mock_reviews(dealer_id)
    
    try:
        db = client[REVIEWS_DB]
        selector = {"selector": {"dealership": {"$eq": int(dealer_id)}}}
        results = db.get_query_result(selector["selector"])
        reviews = list(results)
        client.disconnect()
        return reviews
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        return _mock_reviews(dealer_id)


def save_review(review_data):
    """Save a new review to Cloudant."""
    client = get_database_client()
    if not client:
        logger.info(f"Mock: Would save review: {review_data}")
        return {"ok": True, "id": "mock_id", "rev": "1-mock"}
    
    try:
        db = client[REVIEWS_DB]
        response = db.create_document(review_data)
        client.disconnect()
        return response
    except Exception as e:
        logger.error(f"Error saving review: {e}")
        return None


def _mock_dealers():
    """Return mock dealer data for development."""
    return [
        {"id": 1, "full_name": "Sunshine Toyota", "short_name": "Sunshine", "city": "Wichita", "state": "Kansas", "st": "KS", "address": "123 Main St", "zip": "67201", "lat": 37.69, "long": -97.34},
        {"id": 2, "full_name": "Prairie Ford", "short_name": "Prairie", "city": "Topeka", "state": "Kansas", "st": "KS", "address": "456 Elm Ave", "zip": "66601", "lat": 39.05, "long": -95.68},
        {"id": 3, "full_name": "Lakeside Honda", "short_name": "Lakeside", "city": "Austin", "state": "Texas", "st": "TX", "address": "789 Oak Blvd", "zip": "73301", "lat": 30.27, "long": -97.74},
        {"id": 4, "full_name": "Metro Chevrolet", "short_name": "Metro", "city": "Houston", "state": "Texas", "st": "TX", "address": "321 Pine Rd", "zip": "77001", "lat": 29.76, "long": -95.37},
        {"id": 5, "full_name": "Coastal BMW", "short_name": "Coastal", "city": "Los Angeles", "state": "California", "st": "CA", "address": "654 Sunset Blvd", "zip": "90001", "lat": 34.05, "long": -118.24},
        {"id": 6, "full_name": "Empire Mercedes", "short_name": "Empire", "city": "New York", "state": "New York", "st": "NY", "address": "987 Fifth Ave", "zip": "10001", "lat": 40.71, "long": -74.01},
        {"id": 7, "full_name": "Bluegrass Hyundai", "short_name": "Bluegrass", "city": "Overland Park", "state": "Kansas", "st": "KS", "address": "147 West St", "zip": "66204", "lat": 38.98, "long": -94.67},
        {"id": 8, "full_name": "Gateway VW", "short_name": "Gateway", "city": "Chicago", "state": "Illinois", "st": "IL", "address": "258 Michigan Ave", "zip": "60601", "lat": 41.88, "long": -87.63},
    ]


def _mock_reviews(dealer_id=None):
    """Return mock review data for development."""
    reviews = [
        {"id": "r1", "dealership": 1, "name": "John Smith", "purchase": True, "review": "Fantastic services and very friendly staff!", "purchase_date": "2023-10-15", "car_make": "Toyota", "car_model": "Camry", "car_year": 2023, "sentiment": "positive"},
        {"id": "r2", "dealership": 1, "name": "Jane Doe", "purchase": False, "review": "Great experience overall. Would definitely recommend!", "purchase_date": "", "car_make": "Toyota", "car_model": "RAV4", "car_year": 2022, "sentiment": "positive"},
        {"id": "r3", "dealership": 2, "name": "Bob Johnson", "purchase": True, "review": "Excellent service and fair pricing. Very happy!", "purchase_date": "2023-09-20", "car_make": "Ford", "car_model": "F-150", "car_year": 2023, "sentiment": "positive"},
        {"id": "r4", "dealership": 3, "name": "Alice Williams", "purchase": True, "review": "Amazing dealership! Very helpful and honest team.", "purchase_date": "2023-11-01", "car_make": "Honda", "car_model": "Civic", "car_year": 2023, "sentiment": "positive"},
        {"id": "r5", "dealership": 4, "name": "Charlie Brown", "purchase": False, "review": "Terrible experience. Rude staff and overpriced vehicles.", "purchase_date": "", "car_make": "Chevrolet", "car_model": "Silverado", "car_year": 2022, "sentiment": "negative"},
    ]
    if dealer_id:
        return [r for r in reviews if str(r["dealership"]) == str(dealer_id)]
    return reviews
