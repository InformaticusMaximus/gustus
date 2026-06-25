from django.shortcuts import render
from rest_framework import viewsets
from core.models import Restaurant, URProfile, RExperience, Rating
from .serializers import RestaurantSerializer, URProfileSerializer, RExperienceSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for active restaurants.
    GET /restaurants/ retrieves all active restaurants.
    GET /restaurants/{id}/ retrieves one active restaurant
    """
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class URProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoint for logged in users' restaurant profiles.

    GET /urprofiles/ retrieves all restaurant profiles owned by the user.
    GET /urprofiles/{id}/ retrieve one of the user's restaurant profiles.
    POST /urprofiles/ creates a new restaurant profile for the user.
    PATCH /urprofiles/{id}/ updates selected fields of an existing profile.
    PUT /urprofiles/{id}/ replaces the entire profile.
    DELETE /urprofiles/{id}/ removes a profile.

    Each user can have a single restaurant profile for each restaurant.
    """
    serializer_class = URProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return URProfile.objects.filter(user=self.request.user)

class RExperienceViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoint for logged in users' restaurant experiences.

    GET /urexperiences/ retrieves all restaurant experiences owned by the user.
    GET /urexperiences/{id}/ retrieve one of the user's restaurant experiences.
    POST /urexperiences/ creates a new restaurant experience for the user.
    PATCH /urexperiences/{id}/ updates selected fields of an existing experience.
    PUT /urexperiences/{id}/ replaces the entire experience.
    DELETE /urexperiences/{id}/ removes a experience.
    """
    serializer_class = RExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RExperience.objects.filter(user=self.request.user)

class RatingViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoint for logged in users' ratings.

    GET /ratings/ retrieves all ratings owned by the user.
    GET /ratings/{id}/ retrieve one of the user's ratings.
    POST /ratings/ creates a new rating for the user.
    PATCH /ratings/{id}/ updates selected fields of an existing rating.
    PUT /ratings/{id}/ replaces the entire rating.
    DELETE /ratings/{id}/ removes a rating.

    A user can have one rating for one restaurant experience.
    """
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
