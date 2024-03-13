from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("market:index")
    form = NewUserForm()
    context = {"form": form}
    return render(request, "users/register.html", context)

def login(request):
    return render(request, "users/login.html")