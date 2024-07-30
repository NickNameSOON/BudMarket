# main urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from market.views import index, product_attribute_list
from market.sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('market/', include("market.urls", namespace="market")),
    path('users/', include("users.urls", namespace="users")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('order/', include("order.urls", namespace="order")),
    path('admin/market/productattribute/', product_attribute_list, name='product_attribute_list'),
    path('admin_panel/', include("admin_panel.urls", namespace="admin_panel")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
