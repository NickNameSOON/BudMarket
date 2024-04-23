from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.create_order, name='create-order'),
    path('<int:order_id>/', views.order_detail, name='order-detail'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel-order'),
    path('order_confirmation/', views.order_confirm, name='order-confirmation'),
    path('save-transaction-id', views.save_transaction_id, name='save-transaction-id'),
]
