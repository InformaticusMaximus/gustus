
from rest_framework import serializers
from .models import Restaurant, URProfile
from rest_framework.validators import UniqueTogetherValidator

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "address", "city"]

class URProfileSerializer(serializers.ModelSerializer):
    #HiddenField cuts the field from user output, but still extracts the data for use
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = URProfile
        fields = ["id", "user", "restaurant", "alias", "note"]
        validators = [
                UniqueTogetherValidator(
                    queryset=URProfile.objects.all(),
                    fields=["user", "restaurant"],
                    message="You already have a profile for this restaurant.",
                )
        ]

