from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from core.webpage import html_views


urlpatterns = [
    # Base view
    path("", html_views.home_view, name="home"),
    # GET views
    path("restaurants/", html_views.restaurants_view, name="restaurants"),
    path("urprofiles/", html_views.urprofiles_view, name="urprofiles"),
    path("urexperiences/", html_views.urexperiences_view, name="urexperiences"),
    path("ratings/", html_views.ratings_view, name="ratings"),
    # POST views
    path("urexperiences/add/", html_views.add_urexperience_view, name="add_urexperience"),
    path("ratings/add/", html_views.add_rating_view, name="add_rating"),
    # DELETE views
    path("ratings/<int:rating_id>/delete/", html_views.delete_rating_view, name="delete_rating"),
    path("urexperiences/<int:experience_id>/delete/", html_views.delete_urexperience_view, name="delete_urexperience"),
    # Login/register view
    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", html_views.register_view, name="register"),
    # Top 5
    path("top3/", html_views.top3_view, name="top3"),
    # Search
    path("restaurants/search/", html_views.search_restaurants_view, name="search_restaurants"),
]
