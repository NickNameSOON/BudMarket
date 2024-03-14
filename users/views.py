from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserRegistrationForm, LoginForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:register_done")
        else:
            form = UserRegistrationForm()
    return render(request, "users/register.html", {'form': UserRegistrationForm})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    messages.error(request, f'Invalid username or password')
    return render(request, 'users/login.html', {'form': form})







def register_done(request):  # Перейменована функція входу
    return render(request, "users/register_done.html")