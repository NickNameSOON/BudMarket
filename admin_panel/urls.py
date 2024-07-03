from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.order_list, name='order-list'),
    path('users/', views.user_list, name='user_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),

]
