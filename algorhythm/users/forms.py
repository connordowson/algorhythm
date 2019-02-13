from django import forms
from recommend.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

