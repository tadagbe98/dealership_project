import json
import logging
import requests
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import (
    get_dealers_from_cf,
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    post_review,
    analyze_review_sentiments,
)

logger = logging.getLogger(__name__)


def get_dealerships(request, state="All"):
    """Get all dealerships or filter by state."""
    if state == "All":
        endpoint = "/api/dealership?list"
    else:
        endpoint = f"/api/dealership?list&state={state}"
    
    dealerships = get_dealers_from_cf(endpoint)
    dealers_json = [dealer.__dict__ for dealer in dealerships]
    return JsonResponse({"status": 200, "dealers": dealers_json})


def get_dealer_details(request, dealer_id):
    """Get dealer details by ID."""
    if dealer_id:
        endpoint = f"/api/dealership?id={dealer_id}"
        dealership = get_dealer_by_id_from_cf(endpoint)
        if dealership:
            return JsonResponse({
                "status": 200,
                "dealer": dealership.__dict__
            })
    return JsonResponse({"status": 404, "message": "Dealer not found"})


def get_dealer_reviews(request, dealer_id):
    """Get reviews for a specific dealer."""
    if dealer_id:
        endpoint = f"/api/review?id={dealer_id}"
        reviews = get_dealer_reviews_from_cf(endpoint)
        reviews_json = [review.__dict__ for review in reviews]
        return JsonResponse({"status": 200, "reviews": reviews_json})
    return JsonResponse({"status": 400, "message": "Dealer ID required"})


@csrf_exempt
def add_review(request):
    """Add a review for a dealer."""
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"status": 403, "message": "Unauthorized"})
        
        try:
            data = json.loads(request.body)
            review = {
                "name": f"{request.user.first_name} {request.user.last_name}",
                "dealership": data.get("dealership"),
                "review": data.get("review"),
                "purchase": data.get("purchase", False),
                "purchase_date": data.get("purchase_date", ""),
                "car_make": data.get("car_make", ""),
                "car_model": data.get("car_model", ""),
                "car_year": data.get("car_year", ""),
            }
            
            # Analyze sentiment
            sentiment = analyze_review_sentiments(review["review"])
            review["sentiment"] = sentiment
            
            endpoint = "/api/review"
            result = post_review(endpoint, review)
            return JsonResponse({"status": 200, "result": result})
        except Exception as e:
            logger.error(f"Error adding review: {e}")
            return JsonResponse({"status": 500, "message": str(e)})
    
    return JsonResponse({"status": 405, "message": "Method not allowed"})


@csrf_exempt
def login_request(request):
    """Handle user login."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response_data = {
                    "userName": username,
                    "status": "Authenticated",
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({"userName": username, "status": "Failed"})
        except Exception as e:
            logger.error(f"Login error: {e}")
            return JsonResponse({"status": "Error", "message": str(e)})
    
    return JsonResponse({"status": 405, "message": "Method not allowed"})


@csrf_exempt
def logout_request(request):
    """Handle user logout."""
    username = request.user.username
    logout(request)
    return JsonResponse({"userName": username, "status": "Logged out"})


@csrf_exempt
def registration(request):
    """Handle user registration."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            first_name = data.get("firstName", "")
            last_name = data.get("lastName", "")
            email = data.get("email", "")
            
            # Check if user exists
            try:
                User.objects.get(username=username)
                return JsonResponse({"userName": username, "error": "Already Registered"})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email,
                )
                login(request, user)
                return JsonResponse({
                    "userName": username,
                    "status": "Authenticated",
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                })
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"status": "Error", "message": str(e)})
    
    return JsonResponse({"status": 405, "message": "Method not allowed"})


def get_cars(request):
    """Get all car makes and models."""
    count = CarMake.objects.count()
    if count == 0:
        _initiate_cars()
    
    car_models = CarModel.objects.select_related('car_make')
    cars = [{
        "CarModel": cm.name,
        "CarMake": cm.car_make.name,
        "CarType": cm.get_car_type_display(),
        "ModelYear": cm.year,
        "DealerId": cm.dealer_id,
    } for cm in car_models]
    
    return JsonResponse({"CarModels": cars})


def analyze_review(request):
    """Analyze sentiment of a review text."""
    if request.method == "GET":
        text = request.GET.get("text", "")
        if not text:
            return JsonResponse({"status": 400, "message": "No text provided"})
        
        sentiment = analyze_review_sentiments(text)
        return JsonResponse({"status": 200, "sentiment": sentiment, "text": text})
    
    return JsonResponse({"status": 405, "message": "Method not allowed"})


def _initiate_cars():
    """Populate initial car data."""
    makes_data = [
        {"name": "Toyota", "description": "Japanese automobile manufacturer", "country_of_origin": "Japan", "founded_year": 1937},
        {"name": "Ford", "description": "American automobile manufacturer", "country_of_origin": "USA", "founded_year": 1903},
        {"name": "Honda", "description": "Japanese automobile manufacturer", "country_of_origin": "Japan", "founded_year": 1948},
        {"name": "Chevrolet", "description": "American automobile manufacturer", "country_of_origin": "USA", "founded_year": 1911},
        {"name": "BMW", "description": "German luxury automobile manufacturer", "country_of_origin": "Germany", "founded_year": 1916},
        {"name": "Mercedes-Benz", "description": "German luxury automobile manufacturer", "country_of_origin": "Germany", "founded_year": 1926},
        {"name": "Hyundai", "description": "South Korean automobile manufacturer", "country_of_origin": "South Korea", "founded_year": 1967},
        {"name": "Volkswagen", "description": "German automobile manufacturer", "country_of_origin": "Germany", "founded_year": 1937},
    ]
    
    models_data = [
        {"make": "Toyota", "name": "Camry", "type": "SEDAN", "year": 2023},
        {"make": "Toyota", "name": "RAV4", "type": "SUV", "year": 2022},
        {"make": "Toyota", "name": "Corolla", "type": "SEDAN", "year": 2021},
        {"make": "Ford", "name": "F-150", "type": "TRUCK", "year": 2023},
        {"make": "Ford", "name": "Explorer", "type": "SUV", "year": 2022},
        {"make": "Ford", "name": "Mustang", "type": "COUPE", "year": 2023},
        {"make": "Honda", "name": "Civic", "type": "SEDAN", "year": 2023},
        {"make": "Honda", "name": "CR-V", "type": "SUV", "year": 2022},
        {"make": "Honda", "name": "Accord", "type": "SEDAN", "year": 2021},
        {"make": "Chevrolet", "name": "Silverado", "type": "TRUCK", "year": 2023},
        {"make": "Chevrolet", "name": "Equinox", "type": "SUV", "year": 2022},
        {"make": "BMW", "name": "3 Series", "type": "SEDAN", "year": 2023},
        {"make": "BMW", "name": "X5", "type": "SUV", "year": 2022},
        {"make": "Mercedes-Benz", "name": "C-Class", "type": "SEDAN", "year": 2023},
        {"make": "Mercedes-Benz", "name": "GLE", "type": "SUV", "year": 2022},
        {"make": "Hyundai", "name": "Elantra", "type": "SEDAN", "year": 2023},
        {"make": "Hyundai", "name": "Tucson", "type": "SUV", "year": 2022},
        {"make": "Volkswagen", "name": "Jetta", "type": "SEDAN", "year": 2023},
        {"make": "Volkswagen", "name": "Tiguan", "type": "SUV", "year": 2022},
    ]
    
    make_objects = {}
    for make_data in makes_data:
        make, _ = CarMake.objects.get_or_create(
            name=make_data["name"],
            defaults=make_data
        )
        make_objects[make_data["name"]] = make
    
    for model_data in models_data:
        make = make_objects.get(model_data["make"])
        if make:
            CarModel.objects.get_or_create(
                car_make=make,
                name=model_data["name"],
                defaults={
                    "car_type": model_data["type"],
                    "year": model_data["year"],
                    "dealer_id": None,
                }
            )
