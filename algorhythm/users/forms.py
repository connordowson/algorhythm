from django import forms
from recommend.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
