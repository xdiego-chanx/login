from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import User


# Create your views here.

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def login_verification(request):
    context = {
        "req_user": "",
        "incorrect_credentials": False,
        "no_such_user": False
    }
    if request.method == "POST":
        req_user = request.POST.get("htmluser")
        req_pass = request.POST.get("htmlpass")

        try: 
            requested_user = User.objects.get(username=req_user)
            if check_password(req_pass, requested_user.password):
                context = {
                    "req_user": req_user
                }
                return render(request, "index.html", context, status=302)
            else:
                context = {
                    "incorrect_credentials": True
                }
            return render(request, "login.html", context, status=400)
        except User.DoesNotExist:
            context = {
                "no_such_user": True,
                "req_user": req_user
            }
            return render(request, "login.html", context, status=400)

def signup_verification(request):
    context = {
        "req_user": "",
        "user_exists": False,
        "signup_redirect": False
    }
    if request.method == 'POST':

        req_user = request.POST.get("htmluser")
        req_pass = request.POST.get("htmlpass")

        try:
            User.objects.get(username=req_user)
            context = {
                "user_exists": True,
                "req_user": req_user
            }
            return render(request, "signup.html", context, status=400)
        except User.DoesNotExist:
            new_user = User(username=req_user, password = make_password(req_pass))
            new_user.save()
            context = {
                "signup_redirect": True
            }
            return render(request, "login.html", context, status=302)

def index(request):
    return render(request, "index.html")