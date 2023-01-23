from django.urls import path
from user.views import (
    registration, 
    login, 
    profile

)
urlpatterns = [
    path('', registration, name='user-registration-api'),
    path('login', login, name='user-login-api'),
    path('profile', profile, name='user-profile-api'),


]