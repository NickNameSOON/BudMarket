from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cart.cart import Cart
from market.models import ProductProxy


def cart_view(request):
    return render(request, 'cart/cart-view.html')

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(ProductProxy, id=product_id)
        cart.add(product=product, quantity=product_qty)

    return render(request, 'cart/cart-view.html')

