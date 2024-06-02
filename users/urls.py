from django.urls import path
from .views import register, profile, update_profile, order_update_profile, CustomPasswordChangeView, login_required
from django.contrib.auth.views import LogoutView, LoginView
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView


app_name = "users"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('login_required/', login_required, name="login_required"),
    path('profile/', profile, name="profile"),
    path('profile_update', update_profile, name="update-profile"),
    path('order_profile_update', order_update_profile, name="order-update-profile"),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

