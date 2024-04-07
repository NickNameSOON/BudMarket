import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import Profile



def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "market/index.html", context)


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        product.delete()
        redirect("/market/")
    context = {'product': product}
    return render(request, "market/deleteproduct.html", context=context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    form = CartAddProductForm()
    return render(request, 'market/detail.html', context={'product': product, 'form': form})


def catalog(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    selected_category_slug = request.GET.get('category')

    products = Product.objects.filter(available=True)
    sort_param = request.GET.get('sort')

    if selected_category_slug:
        products = products.filter(category__slug=selected_category_slug)

    if sort_param == 'min_price':
        products = products.order_by('price')
    elif sort_param == 'max_price':
        products = products.order_by('-price')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'market/list.html', {'category': category,
                                                'categories': categories,
                                                'products': products})


def catalog_search(request, category_id):
    # Отримати об'єкт категорії
    category = Category.objects.get(id=category_id)
    # Отримати пошуковий запит та параметр сортування з URL-адреси
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    # Виконати пошук товарів за назвою в межах обраної категорії
    products = Product.objects.filter(category=category)
    if query:
        products = products.filter(name__icontains=query)
    # Виконати сортування за ціною, якщо вибраний відповідний параметр сортування
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    return render(request, 'market/list.html', {'category': category, 'products': products})



def aboutUs(request):
    return render(request, 'market/about_us.html')
