from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.login, name="login_render"),
    path("login-verification/", views.login_verification, name="login_control"),
    path("signup/", views.signup, name="signup_render"),
    path("signup-verification/", views.signup_verification, name="signup_control"),
    path("home/", views.index, name="home")
]