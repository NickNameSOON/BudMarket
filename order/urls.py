from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_confirmation, name='create-order'),
    path('<int:order_id>/', views.order_detail, name='order-detail'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel-order'),
    path('order_confirmation/', views.order_confirmation, name='order-confirmation'),


]
