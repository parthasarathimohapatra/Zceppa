from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    # path('customer/login',CustomerLogin.as_view()),
    path('registration',CustomerRegistration.as_view()),
    path('login',CustomerLogin.as_view()),
    path('profile',UserProfileView.as_view()),
]