#from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login
#from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            upass = form.save(commit=False)
            upass.set_password(form.cleaned_data['password'])
            form.save()
            user = aun
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    return render(request, 'users/profile.html')