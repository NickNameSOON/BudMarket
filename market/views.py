from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductAttribute, ProductAttributeValue
from cart.forms import CartAddProductForm
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, "market/index.html", context)


def index1(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, "market/index1.html", context)


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
    product_attributes = ProductAttributeValue.objects.filter(product=product)
    return render(request, 'market/detail.html',
                  context={'product': product, 'form': form, 'product_attributes': product_attributes})


def catalog(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    brands = Product.objects.values('brand').annotate(count=Count('id')).order_by('brand').distinct()

    selected_category_slug = request.GET.get('category')
    selected_brands = request.GET.getlist('brand')
    sort_param = request.GET.get('sort')
    query = request.GET.get('q', '')

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

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(products, 20)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'market/catalog.html', {
        'category': category,
        'categories': categories,
        'brands': brands,
        'products': products,
        'selected_brands': selected_brands,
        'sort_param': sort_param,
        'query': query,
    })


def aboutUs(request):
    return render(request, 'market/about_us.html')


def product_attribute_list(request):
    category_id = request.GET.get('category__id')
    if category_id:
        attributes = ProductAttribute.objects.filter(category_id=category_id)
        results = [{'id': attr.id, 'text': attr.name} for attr in attributes]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})
