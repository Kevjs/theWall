from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "LandR/index.html")

def register(request):
    errors = User.objects.create_validator(request.POST)
    check = ["first_name","last_name","email"]
    if errors:
        for x in check:
            if x not in errors:
                request.session[x] = request.POST[x]
        for x in errors:
            messages.add_message(request, messages.INFO, errors[x], extra_tags=x)
        return redirect(reverse("login:home"))
    check.append("loginEmail")
    for x in check:
        if x in request.session:
            request.session.pop(x)
    a = User.objects.creator(request.POST)
    request.session["userid"] = a.id
    request.session["username"] = "{} {}".format(a.first_name, a.last_name)
    messages.add_message(request, messages.SUCCESS, f"Welcome {request.session['username']}! You've successfully registered!", extra_tags="welcome")
    return redirect(reverse("theWall:home"))

def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        if "email" not in errors:
            request.session["loginEmail"] = request.POST["email"]
        for x in errors:
            messages.add_message(request, messages.INFO, errors[x], extra_tags=x)
        return redirect(reverse("login:home"))
    else:
        check = ["first_name","last_name","email", "loginEmail"]
        for x in check:
            if x in request.session:
                request.session.pop(x)
        a = User.objects.get(email=request.POST["email"])
        request.session["userid"] = a.id
        request.session["username"] = "{} {}".format(a.first_name, a.last_name)
        messages.add_message(request, messages.SUCCESS, f"Welcome {request.session['username']}!", extra_tags="welcome")
        return redirect(reverse("theWall:home"))

def logout(request):
    if "userid" in request.session:
        request.session.pop("userid")
    if "username" in request.session:
        request.session.pop("username")
    return redirect(reverse("login:home"))