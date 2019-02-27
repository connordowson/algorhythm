from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm, UserRegistrationForm
import bcrypt

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()

            first_name = form.cleaned_data.get('first_name')

            messages.success(request, f'Your accound has been created. Welcome {first_name}')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

# def clean_password(self):

#     password = bytes(self, encoding='utf-8')
#     password = bcrypt.hashpw(password, bcrypt.gensalt())
#     return password