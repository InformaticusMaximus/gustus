from django.contrib import admin
from .models import (Restaurant, EPI, RExperience, Rating, URProfile)

@admin.register(Restaurant, EPI, RExperience, Rating)
class SuperAdmin(admin.ModelAdmin):
    pass

@admin.register(URProfile)
class URProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "restaurant", "alias", "note"]
    list_filder = ["user", "restaurant"]
    search_fields = ["user__name", "restaurant__name", "alias"]
