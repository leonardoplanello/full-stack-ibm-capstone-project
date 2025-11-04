# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


# Create a `get_request` to make HTTP GET requests
def get_request(endpoint, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            backend_url + endpoint, params=kwargs, timeout=5)
        status_code = response.status_code
        json_data = {}
        if status_code == 200:
            json_data = response.json()
            # If json_data is a list, return it directly
            if isinstance(json_data, list):
                return {"status_code": status_code, "json_data": json_data}
        return {"status_code": status_code, "json_data": json_data}
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        # Return empty list if connection fails
        return {"status_code": 500, "json_data": []}
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return {"status_code": 500, "json_data": []}


# Create a `post_request` to make HTTP POST requests
def post_request(endpoint, json_payload, **kwargs):
    try:
        response = requests.post(
            backend_url + endpoint, json=json_payload, params=kwargs)
        status_code = response.status_code
        json_data = {}
        if status_code == 200:
            json_data = response.json()
        return {"status_code": status_code, "json_data": json_data}
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return {"status_code": 500, "json_data": {}}


# Create a `analyze_review_sentiments` method to call the sentiment analysis function
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        status_code = response.status_code
        json_data = {}
        if status_code == 200:
            json_data = response.json()
        return {"status_code": status_code, "json_data": json_data}
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return {"status_code": 500, "json_data": {}}


# Create a `post_review` method to post a review
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        status_code = response.status_code
        json_data = {}
        if status_code == 200:
            json_data = response.json()
        return {"status_code": status_code, "json_data": json_data}
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return {"status_code": 500, "json_data": {}}
