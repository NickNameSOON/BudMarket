from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from market import views

app_name = "market"

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us', views.aboutUs, name='about_us'),
    path('product/<str:product_id>', views.product_detail, name="detail"),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:category_slug>/', views.catalog, name='catalog_by_category'),
    path('sitemap.xml', views.custom_sitemap, name='custom_sitemap'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
