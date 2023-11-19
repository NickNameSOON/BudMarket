from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# Create your views here.
def index(request):
   products = Product.objects.all()
   context = {
       'products': products
   }
   return render(request, "market/index.html", context)

def IndexProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, "market/detail.html", context)
