from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()

            first_name = form.cleaned_data.get('first_name')

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

# def clean_password(self):

#     password = bytes(self, encoding='utf-8')
#     password = bcrypt.hashpw(password, bcrypt.gensalt())
#     return password