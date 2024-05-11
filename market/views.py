from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Count
import logging
from django.views.generic import ListView
from django.db.models import Q


def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
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


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def catalog(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    brands = Product.objects.values('brand').annotate(count=Count('id')).order_by('brand').distinct()

    selected_category_slug = request.GET.get('category')
    selected_brands = request.GET.getlist('brand')
    sort_param = request.GET.get('sort')
    products = Product.objects.filter(available=True)

    if selected_category_slug:
        category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(category=category)

    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    if sort_param == 'min_price':
        products = products.order_by('price')
    elif sort_param == 'max_price':
        products = products.order_by('-price')

    # Setup paginator
    paginator = Paginator(products, 20)  # Відображати 20 товарів на сторінку
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Якщо сторінка не є числом, відображати першу сторінку.
        products = paginator.page(1)
    except EmptyPage:
        # Якщо номер сторінки більший, ніж загальна кількість сторінок, відображати останню сторінку.
        products = paginator.page(paginator.num_pages)

    return render(request, 'market/catalog.html', {
        'category': category,
        'categories': categories,
        'brands': brands,
        'products': products
    })


def catalog_search(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', None)

    logger.debug(f"Query: {query}, Sort by: {sort_by}")

    if query:
        products = Product.objects.filter(title__icontains=query)
        logger.debug(f"Found products: {products.count()}")
    else:
        products = Product.objects.all()

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'market/products_list.html', {'products': products})


def aboutUs(request):
    return render(request, 'market/about_us.html')


class SearchResultsView(ListView):
    model = Product
    template_name = 'market/products_list.html'  # переконайтесь, що це правильний шаблон

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        else:
            return Product.objects.none()