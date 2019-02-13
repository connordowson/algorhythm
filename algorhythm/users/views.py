from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm
import bcrypt

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            new_user = form.save(commit = False)

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password = clean_password(password)
            new_user.password = password
            new_user.save()
            messages.success(request, f'Account created for {email}!')
            return redirect('Index')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def clean_password(self):
    password = bytes(self, encoding='utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    return password