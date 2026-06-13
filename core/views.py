from django.shortcuts import render
from rest_framework import viewsets
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(is_active=True)


