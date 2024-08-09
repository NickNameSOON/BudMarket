# bot/urls.py
from django.urls import path
from . import views

app_name = 'bot'  # Додайте це

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
]
