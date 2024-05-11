from django.urls import path
from market import views
from market.views import SearchResultsView

app_name = "market"

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us', views.aboutUs, name='about_us'),
    path('product/<str:product_id>', views.product_detail, name="detail"),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:category_slug>/', views.catalog, name='catalog_by_category'),
    path('catalog/search/', views.catalog_search, name='catalog_search'),  # змінено URL
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
