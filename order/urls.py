from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.create_order, name='create-order'),
    path('<int:order_id>/', views.order_detail, name='order-detail'),
]
