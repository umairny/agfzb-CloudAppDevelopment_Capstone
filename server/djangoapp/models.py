from django.db import models
from django.utils.timezone import now

# Create a Car Make model
class CarMake(models.Model):
    make = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Make: " + self.make + "des" + self.description

class CarModel(models.Model):
    make_model = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerID = models.IntegerField()
    name = models.CharField(max_length=50)
    CAR_CHOICES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
    )
    type = models.CharField(max_length=50, choices=CAR_CHOICES)
    year = models.DateField(null=True)

    def __str__(self):
        return "Year: " + self.year.strftime('%Y')

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
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
        return "Dealer review: " + self.name
