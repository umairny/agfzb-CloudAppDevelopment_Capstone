from django.http import response
import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs['api_key']))
        else:            
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("POST to {} ".format(url))
    print(json_payload)
    try:
        response = requests.post(url, json_payload, headers={'Content-Type': 'application/json'})
    except Exception as e:
        print("Error", e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    return data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        #print(json_result["dealership"]["rows"])
        dealers = json_result["dealership"]["rows"]
        # For each dealer object
        for dealer in dealers:
            #print(dealer["doc"]["zip"])
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+dealerId)
    #print("reviews ",json_result)
    if "reviews" in json_result:
        reviews = json_result["reviews"]
        #print(reviews)
        # For each review object
        for review in reviews:
            #print(review["purchase"])
            if review["purchase"] == True:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    sentiment=review["review"],
                    id=review["id"],
                    purchase_date=review["purchase_date"],
                    car_make=review["car_make"],
                    car_model=review["car_model"],
                    car_year=review["car_year"],
                )
            else:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    sentiment=review["review"],
                    id=review["id"],
                    purchase_date="",
                    car_make="",
                    car_model="",
                    car_year="",
                )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

# - Parse JSON results into a DealerView object list
def get_dealer_details_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+dealerId)
    #print(json_result)
    details = json_result["dealership"]
    # For each review object
    #print("detials", details)
    for doc in details:
        #print(doc['address'])
        results = CarDealer(
            address=doc["address"], city=doc["city"], full_name=doc["full_name"],
                                id=doc["id"], lat=doc["lat"], long=doc["long"],
                                short_name=doc["short_name"],
                                st=doc["st"], zip=doc["zip"])

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview, **kwargs):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b1af1968-d264-4af9-b645-3f0891234662"
    apikey = "IcaeHW0dXk0Uo7qz228yG9csheCPu3QiAcCoSlvbZoX1"

    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(sentiment=SentimentOptions())).get_result()
    
    # - Get the returned sentiment label such as Positive or Negative
    #print(json.dumps(response, indent=2))
    print("setiment of review: ", response["sentiment"]["document"]["label"])
    sentiment = response["sentiment"]["document"]["label"]
    return sentiment



