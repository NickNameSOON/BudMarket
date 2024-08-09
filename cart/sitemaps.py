# cart/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import CartItem  # Import your model

class CartItemSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return CartItem.objects.all()

    def location(self, item):
        return f'/cart/{item.id}/'
