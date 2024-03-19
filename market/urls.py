from django.urls import path
from market import views

app_name = "market"

urlpatterns = [
    path('', views.index, name='index'),
    path('addproduct/', views.add_product, name="add_product"),
    path('update_product/<int:product_id>/', views.update_product, name="update_product"),
    path('delete_product/<int:product_id>/', views.delete_product, name="delete_product"),
    path('product/<int:product_id>', views.product_detail, name="detail"),
    path('catalog', views.catalog, name='catalog'),
    path('catalog/<str:category_name>/', views.catalog, name='product_list_by_category'),

]