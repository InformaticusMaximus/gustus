"""
The relational database layout for Gustus.
Short docstrings describe each model's function in the domain.
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Restaurant(models.Model):
    """
    A unique restaurant, entry local to the database.
    Stores raw data, identification handled through ExternalPlaceIdentity.
    is_active functions as a soft delete, so that RestaurantExperiences
    after for ex. restaurant closure stay valid for historical purposes.
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    class Meta:
        constraints=[
                models.UniqueConstraint(
                   fields=["name", "address", "city"],
                   condition=models.Q(is_active=True),
                   name="unique_restaurant"
                   )
        ]

    def __str__(self):
        return f"{self.name}, {self.address}, {self.city}, {self.is_active}"

class ExternalPlaceIdentity(models.Model):
    """
    Layer for preventing duplicates.
    Google's place_id from Google Places is planned for integration.
    Adding new Restaurants to the database will be handled through 
    Google Places' API.
    These entries are immutable, and if a place_id becomes obsolete,
    the old one is kept, if the need for it were to arise.
    Identities with is_current=False stop being unique.
    """
    id = models.BigAutoField(primary_key=True)
    external_place_id = models.CharField(max_length=1024)
    provider = models.CharField(max_length=20)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    is_current = models.BooleanField(default=True)
    class Meta:
        constraints=[
                models.UniqueConstraint(
                    fields=["external_place_id", "provider"],
                    condition=models.Q(is_current=True),
                    name="unique_external_place_identity"
                    )
        ]

    def __str__(self):
        return f"{self.external_place_id}, {self.provider}, {self.restaurant}, {self.is_current}"

class RestaurantExperience(models.Model):
    """
    A unique restaurant experience.
    Separates metadata from rating values.
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.user}, {self.restaurant}, {self.date}, {self.time}"

class Rating(models.Model):
    """
    A 5 category rating linked to each RestaurantExperience (1 to 1 relation)
    """
    id = models.BigAutoField(primary_key=True)
    experience = models.OneToOneField(RestaurantExperience, on_delete=models.PROTECT)
    taste = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    quality = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    wait = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    price = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    would_eat_again = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.experience}, {self.taste}, {self.quality}, {self.wait}, {self.price}, {self.would_eat_again}"

class UserRestaurantProfile(models.Model):
    """
    A personalizable restaurant profile for each user.
    Constraint restricts each user to one profile for each restaurant.
    Foreignkeys allow many restaurants to have many profiles for different 
    users, as well as users having one for each restaurant
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    alias = models.CharField(max_length=50, blank=True)
    note = models.CharField(max_length=100, blank=True)
    class Meta:
        constraints=[
                models.UniqueConstraint(
                    fields=["user", "restaurant"],
                    name="unique_user_restaurant_profile")
        ]

    def __str__(self):
        return f"{self.user}, {self.restaurant}, {self.alias}, {self.note}"
