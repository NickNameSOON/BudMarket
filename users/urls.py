from django.urls import path
from .views import register, profile, update_profile
from django.contrib.auth.views import LogoutView, LoginView

app_name = "users"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('profile/', profile, name="profile"),
    path('profile_update', update_profile, name="update-profile"),

]
