from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from core.webpage import html_views


urlpatterns = [
    path("", html_views.home_view, name="home"),
    path("restaurants/", html_views.restaurants_view, name="restaurants"),
    path("urprofiles/", html_views.urprofiles_view, name="urprofiles"),
    path("urexperiences/", html_views.urexperiences_view, name="urexperiences"),
    path("ratings/", html_views.ratings_view, name="ratings"),

    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
]
