from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'release_year', 'genre', 'rating',
                  'running_time', 'content', 'director', 'actors']