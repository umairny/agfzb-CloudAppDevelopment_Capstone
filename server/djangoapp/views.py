from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
import requests
from .models import CarMake, CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_details_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {
        'about' : 'More details about us comming from view'
    }
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {
        'contact' : 'Contact us'
    }
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_req(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_req(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_req(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists try another username."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "http://77abb004.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        #print("Url", url)
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealers"] = dealerships
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "http://77abb004.us-south.apigw.appdomain.cloud/api/review?dealerID="
        urldealer = "http://77abb004.us-south.apigw.appdomain.cloud/api/dealership?dealerID="
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        detail = get_dealer_details_from_cf(urldealer, dealer_id)
        context["reviews"] = reviews
        context["detail"] = detail
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    #print(dealer_id)
    context = {}
    urldealer = "http://77abb004.us-south.apigw.appdomain.cloud/api/dealership?dealerID="
    detail = get_dealer_details_from_cf(urldealer, dealer_id)
    context["detail"] = detail
    context["cars"] = CarModel.objects.all()
    if request.method == 'GET':
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == 'POST':
        #print("car model", request.POST["car"])
        
        car = get_object_or_404(CarModel, pk=request.POST["car"])
        review = {}
        review["name"] = request.user.username
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = int(dealer_id)
        review["review"] = request.POST["content"]
        review["purchase"] = request.POST.get("purchasecheck", False)
        print("check value", review["purchase"])
        if review["purchase"]:
            review["purchase"] = True
            review["car_make"] = car.make_model.make
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
            review["purchase_date"] = request.POST["purchasedate"]

        json_payload = json.dumps(review)
        print(json_payload)
        url = "https://77abb004.us-south.apigw.appdomain.cloud/api/review"
        post_request(url, json_payload)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

