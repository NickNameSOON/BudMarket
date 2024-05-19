from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart, CartItem
from market.models import Product
from cart.forms import CartAddProductForm
from order.models import Order, OrderItem
from django.contrib import messages
from django.db import transaction
from django.urls import reverse


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Перевіряємо, чи товар вже є в кошику
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                # Якщо товар вже є в кошику, збільшуємо кількість
                cart_item.quantity += quantity
            else:
                # Якщо товару немає в кошику, створюємо новий запис
                cart_item.quantity = quantity
            cart_item.save()
            return redirect('cart:cart-view')
    else:
        form = CartAddProductForm()

    return render(request, 'cart/cart_view.html', {'form': form})


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = cart.get_total_price()
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart/cart_view.html', context)


def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(pk=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart:cart-view')


def decrease_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return JsonResponse({'success': True})
    else:
        cart_item.delete()
        return JsonResponse({'success': False})


@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                # Якщо кількість введена неправильно, можна видалити товар з кошика
                cart_item.delete()
    return redirect('cart:cart-view')


