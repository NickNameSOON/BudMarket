# main urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from market.views import index, product_attribute_list
from .sitemaps import urlpatterns as sitemap_urls


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('market/', include("market.urls", namespace="market")),
    path('users/', include("users.urls", namespace="users")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('order/', include("order.urls", namespace="order")),
    path('admin/market/productattribute/', product_attribute_list, name='product_attribute_list'),
    path('admin_panel/', include("admin_panel.urls", namespace="admin_panel")),
<<<<<<< HEAD
    path('', include('market.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')),
    path('', include('users.urls')),
] + sitemap_urls
=======
    path('bot/', include("bot.urls", namespace="bot")),
]
>>>>>>> refs/remotes/origin/master

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
