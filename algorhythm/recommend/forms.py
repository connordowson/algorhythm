from django.contrib.auth.models import User
from .models import Song, UserTopTracks, User, Recommendation
from django import forms

class FeedbackForm(forms.Form):
    song_id = 