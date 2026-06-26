"""
Views for the HTML site.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Restaurant, URProfile, RExperience, Rating
from core.forms import URExperienceForm, RatingForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from core.recommendations import TopXEngine, RepeatInterestWeightStrategy, NotEnoughRatedRestaurantsError
from django.core.paginator import Paginator

def home_view(request):
    return render(request, "core/home.html")

def restaurants_view(request):
    restaurants = (
        Restaurant.objects
        .filter(is_active=True)
        .order_by("name")
    )

    return render(
        request,
        "core/restaurants.html",
        {"restaurants": restaurants},
    )

@login_required
def urprofiles_view(request):
    profiles = (
            URProfile.objects
            .filter(user=request.user)
            .select_related("restaurant")
            .order_by("restaurant__name")
    )

    return render(request, "core/urprofiles.html", {"profiles":profiles})

# URExperience
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
def add_urexperience_view(request):
    if request.method == "POST":
        form = URExperienceForm(request.POST)

        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()

            return redirect("urexperiences")
    else:
        form = URExperienceForm()

    return render(
        request,
        "core/add_urexperience.html",
        {"form": form},
    )

@login_required
def delete_urexperience_view(request, experience_id):
    experience = get_object_or_404(
        RExperience,
        id=experience_id,
        user=request.user,
    )

    if request.method == "POST":
        try:
            experience.delete()
            messages.success(request, "Experience deleted successfully.")
        except ProtectedError:
            messages.error(
                request,
                "This experience has a rating attached, please delete the rating first.",
            )

    return redirect("urexperiences")

@login_required
def ratings_view(request):
    ratings = (
        Rating.objects
        .filter(user=request.user)
        .select_related("experience", "experience__restaurant")
        .order_by("-id")
    )

    return render(request, "core/ratings.html", {"ratings": ratings})

@login_required
def add_rating_view(request):
    if request.method == "POST":
        form = RatingForm(request.POST)
        form.fields["experience"].queryset = RExperience.objects.filter(
            user=request.user,
            rating__isnull=True,
        )

        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.save()

            return redirect("ratings")
    else:
        form = RatingForm()
        form.fields["experience"].queryset = RExperience.objects.filter(
            user=request.user,
            rating__isnull=True,
        )

    return render(
        request,
        "core/add_rating.html",
        {"form": form},
    )

@login_required
def delete_rating_view(request, rating_id):
    rating = get_object_or_404(
        Rating,
        id=rating_id,
        user=request.user,
    )

    if request.method == "POST":
        rating.delete()
        messages.success(request, "Rating deleted successfully.")

    return redirect("ratings")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(
        request,
        "core/register.html",
        {"form": form},
    )

@login_required
def top3_view(request):
    engine = TopXEngine(
            min_restaurants=3,
            limit=3,
            strategy=RepeatInterestWeightStrategy()
            )

    try:
        recommendations = engine.get_top_restaurants(request.user)
        error_message = None
    except NotEnoughRatedRestaurantsError as error:
        recommendations = []
        error_message = str(error)

    return render(
        request,
        "core/top3.html",
        {
            "recommendations": recommendations,
            "error_message": error_message,
        },
    )

def search_restaurants_view(request):
    query = request.GET.get("q", "")
    city = request.GET.get("city", "")
    sort = request.GET.get("sort", "name")

    restaurants = Restaurant.objects.filter(is_active=True)

    if query:
        restaurants = restaurants.filter(name__icontains=query)

    if city:
        restaurants = restaurants.filter(city__icontains=city)

    if sort == "city":
        restaurants = restaurants.order_by("city", "name")
    else:
        restaurants = restaurants.order_by("name")

    paginator = Paginator(restaurants, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "core/search_restaurants.html",
        {
            "page_obj": page_obj,
            "query": query,
            "city": city,
            "sort": sort,
        },
    )
