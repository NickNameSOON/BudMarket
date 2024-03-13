from django.urls import path
from market import views

app_name = "market"

urlpatterns = [
    path('index', views.index, name="index"),
    path('', views.index),
    path('<int:product_id>/', views.IndexProduct, name="detail"),
    path('addproduct', views.add_product, name="add_product"),
    path('update_product/<int:product_id>', views.update_product, name="update_product"),
    path('delete_product/<int:product_id>', views.delete_product, name="delete_product"),


]