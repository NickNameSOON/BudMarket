#from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login
#from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            upass = form.save(commit=False)
            upass.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('/')  # Перенаправлення після успішної реєстрації
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})




'''def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users/register_done.html")
        else:
            form = UserRegistrationForm()
    return render(request, "users/register.html", {'form': UserRegistrationForm})
'''

def register_done(request):
    return render(request, "users/register_done.html")

@login_required
def profile(request):
    return render(request, 'users/profile.html')