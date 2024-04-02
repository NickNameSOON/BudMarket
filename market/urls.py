from django.urls import path
from market import views

app_name = "market"

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<str:product_id>', views.product_detail, name="detail"),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:category_slug>/', views.catalog, name='catalog_by_category'),

]