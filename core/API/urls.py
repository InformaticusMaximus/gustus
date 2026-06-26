"""
URL configuration for Gustus's API.

Built on Django's DefaultRouter entirely.
"""

from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, URProfileViewSet, RExperienceViewSet, RatingViewSet

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("urprofiles", URProfileViewSet, basename="urprofile")
router.register("urexperiences", RExperienceViewSet, basename="urexperience")
router.register("ratings", RatingViewSet, basename="rating")
urlpatterns = router.urls
