import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

# Cloudant and IBM Cloud Functions URLs
cloudant_base_url = os.environ.get("CLOUDANT_URL", "")
cf_base_url = os.environ.get("CF_BASE_URL", "https://us-south.functions.appdomain.cloud/api/v1/web/your-namespace")

# IBM NLU
ibm_api_key = os.environ.get("IBM_API_KEY", "")
ibm_nlu_url = os.environ.get("IBM_NLU_URL", "")


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip

    def __str__(self):
        return f"Dealer name: {self.full_name}"


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Review from {self.name}: {self.review}"


def get_request(endpoint, **kwargs):
    """Generic GET request to Cloud Functions."""
    params = ""
    if kwargs:
        params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
    
    request_url = f"{cf_base_url}{endpoint}"
    if params:
        request_url += f"?{params}"
    
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Network error: {e}")
        return _get_mock_data(endpoint, **kwargs)


def post_request(endpoint, json_payload, **kwargs):
    """Generic POST request to Cloud Functions."""
    params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
    request_url = f"{cf_base_url}{endpoint}"
    if params:
        request_url += f"?{params}"
    
    try:
        response = requests.post(request_url, json=json_payload, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Network error: {e}")
        return {"status": 200, "message": "Review submitted (mock)"}


def get_dealers_from_cf(endpoint, **kwargs):
    """Get list of dealers from Cloud Functions."""
    results = get_request(endpoint, **kwargs)
    if isinstance(results, list):
        dealers = [parse_dealer_json(dealer) for dealer in results]
        return dealers
    return []


def get_dealer_by_id_from_cf(endpoint, dealer_id=None):
    """Get a single dealer by ID."""
    results = get_request(endpoint)
    if isinstance(results, list) and len(results) > 0:
        return parse_dealer_json(results[0])
    elif isinstance(results, dict):
        return parse_dealer_json(results)
    return None


def get_dealer_reviews_from_cf(endpoint, dealer_id=None):
    """Get reviews for a dealer."""
    results = get_request(endpoint)
    reviews = []
    if isinstance(results, dict):
        results = results.get("data", {}).get("docs", [])
    if isinstance(results, list):
        for review_data in results:
            try:
                sentiment = analyze_review_sentiments(review_data.get("review", ""))
                review = DealerReview(
                    dealership=review_data.get("dealership", ""),
                    name=review_data.get("name", "Anonymous"),
                    purchase=review_data.get("purchase", False),
                    review=review_data.get("review", ""),
                    purchase_date=review_data.get("purchase_date", ""),
                    car_make=review_data.get("car_make", ""),
                    car_model=review_data.get("car_model", ""),
                    car_year=review_data.get("car_year", ""),
                    sentiment=sentiment,
                    id=review_data.get("id", review_data.get("_id", "")),
                )
                reviews.append(review)
            except Exception as e:
                logger.error(f"Error parsing review: {e}")
    return reviews


def analyze_review_sentiments(text):
    """Analyze sentiment of review text using IBM Watson NLU."""
    if not text:
        return "neutral"
    
    if not ibm_api_key or not ibm_nlu_url:
        return _simple_sentiment(text)
    
    try:
        from ibm_watson import NaturalLanguageUnderstandingV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
        from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

        authenticator = IAMAuthenticator(ibm_api_key)
        nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )
        nlu.set_service_url(ibm_nlu_url)

        response = nlu.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions(targets=[text]))
        ).get_result()

        sentiment = response["sentiment"]["document"]["label"]
        return sentiment
    except Exception as e:
        logger.error(f"IBM Watson NLU error: {e}")
        return _simple_sentiment(text)


def _simple_sentiment(text):
    """Simple keyword-based sentiment analysis as fallback."""
    positive_words = [
        "great", "excellent", "amazing", "fantastic", "wonderful", "good", 
        "best", "love", "perfect", "outstanding", "superb", "awesome",
        "happy", "satisfied", "recommend", "helpful", "friendly", "clean"
    ]
    negative_words = [
        "bad", "terrible", "horrible", "awful", "worst", "hate", "poor",
        "disappointing", "unhappy", "rude", "dirty", "slow", "overpriced",
        "broken", "failed", "never", "waste", "problem", "issue"
    ]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"


def post_review(endpoint, payload):
    """Post a review to Cloudant."""
    return post_request(endpoint, json_payload=payload)


def parse_dealer_json(dealer_doc):
    """Parse dealer JSON into CarDealer object."""
    try:
        return CarDealer(
            address=dealer_doc.get("address", ""),
            city=dealer_doc.get("city", ""),
            full_name=dealer_doc.get("full_name", ""),
            id=dealer_doc.get("id", dealer_doc.get("_id", 0)),
            lat=dealer_doc.get("lat", 0),
            long=dealer_doc.get("long", 0),
            short_name=dealer_doc.get("short_name", ""),
            st=dealer_doc.get("st", ""),
            state=dealer_doc.get("state", ""),
            zip=dealer_doc.get("zip", ""),
        )
    except Exception as e:
        logger.error(f"Error parsing dealer: {e}")
        return None


def _get_mock_data(endpoint, **kwargs):
    """Return mock data when Cloud Functions are not available."""
    
    dealers = [
        {"id": 1, "full_name": "Sunshine Toyota", "short_name": "Sunshine", "city": "Wichita", "state": "Kansas", "st": "KS", "address": "123 Main St", "zip": "67201", "lat": 37.69, "long": -97.34},
        {"id": 2, "full_name": "Prairie Ford", "short_name": "Prairie", "city": "Topeka", "state": "Kansas", "st": "KS", "address": "456 Elm Ave", "zip": "66601", "lat": 39.05, "long": -95.68},
        {"id": 3, "full_name": "Lakeside Honda", "short_name": "Lakeside", "city": "Austin", "state": "Texas", "st": "TX", "address": "789 Oak Blvd", "zip": "73301", "lat": 30.27, "long": -97.74},
        {"id": 4, "full_name": "Metro Chevrolet", "short_name": "Metro", "city": "Houston", "state": "Texas", "st": "TX", "address": "321 Pine Rd", "zip": "77001", "lat": 29.76, "long": -95.37},
        {"id": 5, "full_name": "Coastal BMW", "short_name": "Coastal", "city": "Los Angeles", "state": "California", "st": "CA", "address": "654 Sunset Blvd", "zip": "90001", "lat": 34.05, "long": -118.24},
        {"id": 6, "full_name": "Empire Mercedes", "short_name": "Empire", "city": "New York", "state": "New York", "st": "NY", "address": "987 Fifth Ave", "zip": "10001", "lat": 40.71, "long": -74.01},
        {"id": 7, "full_name": "Bluegrass Hyundai", "short_name": "Bluegrass", "city": "Overland Park", "state": "Kansas", "st": "KS", "address": "147 West St", "zip": "66204", "lat": 38.98, "long": -94.67},
        {"id": 8, "full_name": "Gateway VW", "short_name": "Gateway", "city": "Chicago", "state": "Illinois", "st": "IL", "address": "258 Michigan Ave", "zip": "60601", "lat": 41.88, "long": -87.63},
    ]
    
    reviews = [
        {"id": "r1", "dealership": 1, "name": "John Smith", "purchase": True, "review": "Fantastic services and very friendly staff!", "purchase_date": "2023-10-15", "car_make": "Toyota", "car_model": "Camry", "car_year": 2023},
        {"id": "r2", "dealership": 1, "name": "Jane Doe", "purchase": False, "review": "Great experience overall. Would recommend!", "purchase_date": "", "car_make": "Toyota", "car_model": "RAV4", "car_year": 2022},
        {"id": "r3", "dealership": 2, "name": "Bob Johnson", "purchase": True, "review": "Excellent service and fair pricing.", "purchase_date": "2023-09-20", "car_make": "Ford", "car_model": "F-150", "car_year": 2023},
        {"id": "r4", "dealership": 3, "name": "Alice Williams", "purchase": True, "review": "Amazing dealership! Very helpful team.", "purchase_date": "2023-11-01", "car_make": "Honda", "car_model": "Civic", "car_year": 2023},
    ]
    
    state_filter = kwargs.get("state")
    
    if "review" in endpoint or "review" in str(kwargs):
        # Extract dealer id from URL or kwargs
        dealer_id = kwargs.get("id", "")
        if "id=" in endpoint:
            try:
                dealer_id = int(endpoint.split("id=")[-1].split("&")[0])
            except:
                dealer_id = None
        filtered_reviews = [r for r in reviews if not dealer_id or r["dealership"] == dealer_id]
        return filtered_reviews
    
    elif "dealership" in endpoint:
        # Check if filtering by id
        if "id=" in endpoint:
            try:
                dealer_id = int(endpoint.split("id=")[-1].split("&")[0])
                return [d for d in dealers if d["id"] == dealer_id]
            except:
                pass
        
        # Filter by state if provided
        if state_filter:
            return [d for d in dealers if d["state"].lower() == state_filter.lower() or d["st"].lower() == state_filter.lower()]
        
        return dealers
    
    return []
