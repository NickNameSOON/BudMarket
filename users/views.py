from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from order.models import Order
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            form.save()
            authenticate(username=username, password=password, password2=password2, email=email)
            login(request, profile)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
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
    active_orders = Order.objects.filter(user=user, status__in=['Опрацювання', 'Комплектація', 'Доставляється']).order_by('-created_at')
    inactive_orders = Order.objects.filter(user=user, status__in=['Отримано покупцем', 'Відмінено']).order_by('-created_at')

    context = {
        'user': user,
        'profile': profile,
        'active_orders': active_orders,
        'inactive_orders': inactive_orders,
    }

    return render(request, 'users/profile.html', context=context)


def login_required(request):
    return render(request, 'users/login_required.html')


def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile_update.html', {'form': form})


def order_update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('order:order-confirmation')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/oder_profile_update.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
