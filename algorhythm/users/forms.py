from django import forms
from django.contrib.auth.forms import UserCreationForm
from recommend.models import User

class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']