from django.urls import path
from market import views

app_name = "market"

urlpatterns = [
    path('', views.index, name='index'),
    path('index1', views.index1, name='index1'),
    path('about-us', views.aboutUs, name='about_us'),
    path('product/<str:product_id>', views.product_detail, name="detail"),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:category_slug>/', views.catalog, name='catalog_by_category'),
]
