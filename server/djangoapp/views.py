# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from . import restapis
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except Exception:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "/fetchDealers"
        dealerships = restapis.get_request(url)
        context["dealers"] = dealerships["json_data"]
        return JsonResponse({"status": 200, "dealers": dealerships["json_data"]})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if request.method == "GET":
        url = f"/fetchReviews/dealer/{dealer_id}"
        reviews = restapis.get_request(url)
        dealer_reviews = reviews["json_data"]
        
        # Analyze sentiment for each review
        for review in dealer_reviews:
            sentiment_result = restapis.analyze_review_sentiments(review.get("review", ""))
            if sentiment_result.get("json_data"):
                review["sentiment"] = sentiment_result["json_data"].get("sentiment", "neutral")
            else:
                review["sentiment"] = "neutral"
        
        return JsonResponse({"status": 200, "reviews": dealer_reviews})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"/fetchDealer/{dealer_id}"
        dealer = restapis.get_request(url)
        return JsonResponse({"status": 200, "dealer": dealer["json_data"]})


# Create a `get_dealerships` view to fetch dealers by state
def get_dealerships_by_state(request, state):
    if request.method == "GET":
        url = f"/fetchDealers/{state}"
        dealerships = restapis.get_request(url)
        return JsonResponse({"status": 200, "dealers": dealerships["json_data"]})


# Create a `get_cars` view to get all car makes and models
def get_cars(request):
    if request.method == "GET":
        cars = []
        car_models = CarModel.objects.select_related('car_make').all()
        for car_model in car_models:
            cars.append({
                "CarMake": car_model.car_make.name,
                "CarModel": car_model.name,
                "CarYear": car_model.year
            })
        return JsonResponse({"CarModels": cars})


# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        # Get user information
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"status": 401, "error": "User not authenticated"})
        
        # Prepare review data
        review_data = {
            "name": f"{user.first_name} {user.last_name}".strip() or user.username,
            "dealership": data.get("dealership"),
            "review": data.get("review"),
            "purchase": data.get("purchase", False),
            "purchase_date": data.get("purchase_date"),
            "car_make": data.get("car_make"),
            "car_model": data.get("car_model"),
            "car_year": data.get("car_year"),
        }
        
        # Post review to backend
        result = restapis.post_review(review_data)
        
        if result.get("status_code") == 200:
            return JsonResponse({"status": 200, "message": "Review added successfully"})
        else:
            return JsonResponse({"status": 500, "error": "Failed to add review"})
