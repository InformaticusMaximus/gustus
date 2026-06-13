
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, URProfileViewSet

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("urprofiles", URProfileViewSet, basename="urprofile")
urlpatterns = router.urls
