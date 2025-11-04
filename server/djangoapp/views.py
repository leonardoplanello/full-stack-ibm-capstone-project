# Uncomment the required imports before adding the code

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
import logging
import json
import os
from django.views.decorators.csrf import csrf_exempt
from . import restapis
from .models import CarModel

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
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
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
    if request.method == "GET":
        url = "/fetchDealers"
        dealerships = restapis.get_request(url)
        dealers_data = dealerships["json_data"]

        # If no data from Express, try to load from JSON file as fallback
        if not dealers_data or (isinstance(dealers_data, list) and len(dealers_data) == 0):
            try:
                json_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'data', 'dealerships.json')
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        json_data = json.load(f)
                        dealers_data = json_data.get('dealerships', [])
            except Exception as e:
                logger.error(f"Error loading dealerships from file: {e}")
                dealers_data = []

        # Ensure dealers_data is a list
        if not isinstance(dealers_data, list):
            if isinstance(dealers_data, dict) and "dealerships" in dealers_data:
                dealers_data = dealers_data["dealerships"]
            elif isinstance(dealers_data, dict):
                dealers_data = []
        return JsonResponse({"status": 200, "dealers": dealers_data})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if request.method == "GET":
        url = f"/fetchReviews/dealer/{dealer_id}"
        reviews = restapis.get_request(url)
        dealer_reviews = reviews["json_data"]

        # If no data from Express, try to load from JSON file as fallback
        if not dealer_reviews or (isinstance(dealer_reviews, list) and len(dealer_reviews) == 0):
            try:
                json_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'data', 'reviews.json')
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        json_data = json.load(f)
                        all_reviews = json_data.get('reviews', [])
                        # Filter by dealer_id
                        dealer_reviews = [review for review in all_reviews if review.get('dealership') == dealer_id]
            except Exception as e:
                logger.error(f"Error loading reviews from file: {e}")
                dealer_reviews = []

        # Ensure dealer_reviews is a list
        if not isinstance(dealer_reviews, list):
            if isinstance(dealer_reviews, dict):
                dealer_reviews = []

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
        dealer_data = dealer["json_data"]

        # If no data from Express, try to load from JSON file as fallback
        if not dealer_data or (isinstance(dealer_data, list) and len(dealer_data) == 0):
            try:
                json_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'data', 'dealerships.json')
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        json_data = json.load(f)
                        all_dealers = json_data.get('dealerships', [])
                        # Find dealer by ID
                        dealer_found = None
                        for d in all_dealers:
                            if d.get('id') == dealer_id:
                                dealer_found = d
                                break
                        dealer_data = [dealer_found] if dealer_found else []
            except Exception as e:
                logger.error(f"Error loading dealer from file: {e}")
                dealer_data = []

        # Ensure dealer_data is a list (React component expects an array)
        if not isinstance(dealer_data, list):
            if isinstance(dealer_data, dict):
                dealer_data = [dealer_data]
            else:
                dealer_data = []

        return JsonResponse({"status": 200, "dealer": dealer_data})


# Create a `get_dealerships` view to fetch dealers by state
def get_dealerships_by_state(request, state):
    if request.method == "GET":
        url = f"/fetchDealers/{state}"
        dealerships = restapis.get_request(url)
        dealers_data = dealerships["json_data"]

        # If no data from Express, try to load from JSON file as fallback and filter locally
        if not dealers_data or (isinstance(dealers_data, list) and len(dealers_data) == 0):
            try:
                json_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'data', 'dealerships.json')
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        json_data = json.load(f)
                        all_dealers = json_data.get('dealerships', [])
                        # Filter by state
                        dealers_data = [dealer for dealer in all_dealers if dealer.get('state') == state]
            except Exception as e:
                logger.error(f"Error loading dealerships from file: {e}")
                dealers_data = []

        # Ensure dealers_data is a list
        if not isinstance(dealers_data, list):
            if isinstance(dealers_data, dict) and "dealerships" in dealers_data:
                dealers_data = dealers_data["dealerships"]
            elif isinstance(dealers_data, dict):
                dealers_data = []

        return JsonResponse({"status": 200, "dealers": dealers_data})


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
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": 400, "error": "Invalid JSON"})

        # Prepare review data (use data from request since React sends it)
        review_data = {
            "name": data.get("name", "Anonymous"),
            "dealership": data.get("dealership"),
            "review": data.get("review"),
            "purchase": data.get("purchase", False),
            "purchase_date": data.get("purchase_date"),
            "car_make": data.get("car_make"),
            "car_model": data.get("car_model"),
            "car_year": data.get("car_year"),
        }

        # Validate required fields
        if not all([review_data["dealership"], review_data["review"], review_data["purchase_date"],
                   review_data["car_make"], review_data["car_model"], review_data["car_year"]]):
            return JsonResponse({"status": 400, "error": "All fields are required"})

        # Post review to backend
        result = restapis.post_review(review_data)

        # If backend fails, save to JSON file as fallback
        if result.get("status_code") != 200:
            try:
                json_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'data', 'reviews.json')
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        json_data = json.load(f)

                    # Add new review
                    new_review = {
                        "id": len(json_data.get('reviews', [])) + 1,
                        "name": review_data["name"],
                        "dealership": int(review_data["dealership"]),
                        "review": review_data["review"],
                        "purchase": review_data["purchase"],
                        "purchase_date": review_data["purchase_date"],
                        "car_make": review_data["car_make"],
                        "car_model": review_data["car_model"],
                        "car_year": int(review_data["car_year"])
                    }

                    if 'reviews' not in json_data:
                        json_data['reviews'] = []

                    json_data['reviews'].append(new_review)

                    # Write back to file
                    with open(json_path, 'w') as f:
                        json.dump(json_data, f, indent=2)

                    logger.info(f"Review saved to JSON file: {new_review['id']}")
            except Exception as e:
                logger.error(f"Error saving review to JSON file: {e}")

        return JsonResponse({"status": 200, "message": "Review added successfully"})
