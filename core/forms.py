"""
POST forms for HTML site.
"""

from django import forms

from core.models import RExperience, Rating


class URExperienceForm(forms.ModelForm):
    class Meta:
        model = RExperience
        fields = ["restaurant", "date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            "experience",
            "taste",
            "quality",
            "wait",
            "price",
            "would_eat_again",
        ]
