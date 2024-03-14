from django.urls import path
from .views import register, register_done, user_login
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('register_done/', register_done, name="register"),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name="logout")
]