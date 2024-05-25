from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', views.cart, name='cart-view'),
    path('update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
]