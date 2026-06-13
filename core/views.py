from django.shortcuts import render
from rest_framework import viewsets
from .models import Restaurant, URProfile
from .serializers import RestaurantSerializer, URProfileSerializer
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
