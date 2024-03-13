from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product




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
        item = Product(name=name, price=price, description=description, image=image)
        item.save()

    return render(request, "market/addproduct.html")


def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.image = request.FILES.get('upload' ,)
        product.save()
        redirect("/market/")
    context = {'product': product}
    return render(request, "market/update_product.html", context=context)


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        product.delete()
        redirect("/market/")
    context = {'product': product}
    return render(request, "market/deleteproduct.html", context=context)
