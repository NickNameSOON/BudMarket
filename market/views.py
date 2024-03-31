from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "market/index.html", context)


@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        seller = request.POST.get("seller")
        description = request.POST.get("description")
        image = request.FILES['upload']

        item = Product(name=name, price=price, description=description, image=image, seller=seller)
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


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request,'market/detail.html', context={'product': product})


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
