# BudMarket/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from market.sitemaps import ProductSitemap
from cart.sitemaps import CartItemSitemap
from order.sitemaps import OrderSitemap
from users.sitemaps import UserSitemap

sitemaps = {
    'products': ProductSitemap,
    'cart_items': CartItemSitemap,
    'orders': OrderSitemap,
    'users': UserSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
