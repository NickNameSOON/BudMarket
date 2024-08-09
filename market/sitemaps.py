# market/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Product  # Import your model

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, item):
        return f'/market/{item.slug}/'
