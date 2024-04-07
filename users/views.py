from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from .models import Profile
from order.models import Order

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    profile = user.profile

    # Отримуємо активні замовлення користувача
    active_orders = Order.objects.filter(user=user)

    # Отримуємо історію замовлень користувача
    order_history = Order.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profile,
        'active_orders': active_orders,
        'order_history': order_history,
    }

    return render(request, 'users/profile.html', context)

def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Після успішного оновлення перенаправте користувача на головну сторінку або на іншу відповідну сторінку
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile_update.html', {'form': form})
