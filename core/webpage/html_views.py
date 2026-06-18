from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Restaurant, URProfile, RExperience, Rating

def home_view(request):
    return render(request, "core/home.html")

def restaurants_view(request):
    restaurants = (
            Restaurant.objects
            .filter(is_active=True)
            .order_by("name")
    )
    return render(request, "core/restaurants.html", {"restaurants":restaurants})

@login_required
def urprofiles_view(request):
    profiles = (
            URProfile.objects
            .filter(user=request.user)
            .select_related("restaurant")
            .order_by("restaurant__name")
    )

    return render(request, "core/urprofiles.html", {"profiles":profiles})


@login_required
def urexperiences_view(request):
    experiences = (
        RExperience.objects
        .filter(user=request.user)
        .select_related("restaurant")
        .order_by("-date", "-time")
    )

    return render(request, "core/urexperiences.html", {"experiences": experiences})


@login_required
def ratings_view(request):
    ratings = (
        Rating.objects
        .filter(user=request.user)
        .select_related("experience", "experience__restaurant")
        .order_by("-id")
    )

    return render(request, "core/ratings.html", {"ratings": ratings})
