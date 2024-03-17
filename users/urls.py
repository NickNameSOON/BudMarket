from django.urls import path
from .views import register, register_done, profile
from django.contrib.auth.views import LogoutView, LoginView

app_name = "users"

urlpatterns = [
    path('register/', register, name="register"),
    path('register_done/', register_done, name="register"),
    path('login/', LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('profile/', profile, name="profile"),

]