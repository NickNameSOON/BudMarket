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
    context = {'product': product}
    return render(request, "market/detail.html", context=context)


def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES['upload']
        Product = Product(name=name, price=price, description=description, image=image)
        Product.save()

    return render(request, "market/addproduct.html")
