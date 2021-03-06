"""algorhythm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import handler404, handler500

from users import views as user_views
from recommend import views as recommend_views

handler404 = 'recommend.views.view_404'
handler500 = 'recommend.views.view_500'


urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),
    path('register/', user_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),

    path('', recommend_views.index, name = 'index'),
    path('recommend/', recommend_views.recommend, name = 'recommend'),
    path('recommendations/', recommend_views.recommendations, name = 'recommendations'),
    path('feedback/', recommend_views.feedback, name = 'feedback'),
    path('feedback_submit/', recommend_views.feedback, name = 'feedback submit'),
    path('recommend/short_term/', recommend_views.short_term, name = 'Short term'),
    path('recommend/medium_term/', recommend_views.medium_term, name = 'Medium term'),
    path('recommend/long_term/', recommend_views.long_term, name = 'Long term'),

]

