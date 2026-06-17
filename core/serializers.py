
from rest_framework import serializers
from .models import Restaurant, URProfile, RExperience, Rating
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

class RExperienceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RExperience
        fields = ["id", "user", "restaurant", "date", "time"]
        
class RatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = ["id", "user", "experience", "taste", "quality", "wait", "price", "would_eat_again"]
        
        def validate_experience(self, experience):
            request = self.context["request"]

            if experience.user != request.user:
                raise serializers.ValidationError("This experience does not belong to you.")

            if Rating.objects.filter(experience=experience).exists():
                raise serializers.ValidationError("You already posted a rating for this experience. Please update it instead.")

            return experience
