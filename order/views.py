import json
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PurchaseForm, PaymentForm, DeliveryForm
from .models import Order, OrderItem
from cart.models import CartItem, Cart
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def order_confirm(request):
    user = request.user
    profile = user.profile
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = cart.get_total_price()
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'user': user,
        'profile': profile,
    }
    return render(request, 'order/confirmation.html', context=context)


@login_required
def create_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Кошик не знайдено.")
        return redirect('cart:cart-view')

    if request.method == 'GET':
        # Відображення сторінки підтвердження
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'order/order_confirmation.html', {'cart_items': cart_items, 'total_price': total_price})

    elif request.method == 'POST':
        delivery_method = request.POST.get('deliveryMethod')
        payment_method = request.POST.get('paymentMethod')  # Переконайтеся, що поле paymentMethod відправляється формою

        # Обробка форми доставки
        if delivery_method == 'delivery':
            delivery_form = DeliveryForm(request.POST)
            if delivery_form.is_valid():
                delivery_address = delivery_form.cleaned_data['delivery_address']
                # Логіка створення замовлення для доставки
                return process_order(request, cart, delivery_address=delivery_address)
            else:
                messages.error(request, "Перевірте введені дані у формі доставки.")
                return redirect('order:order-confirmation')

        # Обробка замовлення без доставки (самовивіз)
        return process_order(request, cart)

def process_order(request, cart, delivery_address=None):
    with transaction.atomic():
        order = Order.objects.create(user=request.user, delivery_address=delivery_address)
        total_price = 0
        for cart_item in cart.cartitem_set.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price * cart_item.quantity
            )
            total_price += order_item.price

        order.total_price = total_price
        order.save()

        # Очищення кошика після створення замовлення
        cart.cartitem_set.all().delete()

        return redirect(reverse('order:order-detail', kwargs={'order_id': order.id}))


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.user != request.user:
        # Якщо користувач не є власником замовлення, перенаправляємо його на сторінку заборони
        return HttpResponseForbidden("You don't have permission to view this order.")
    return render(request, 'order/order_detail.html', {'order': order})


def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.status = Order.CANCELED
        order.save()
        return redirect('order:order-detail', order_id=order_id)
    return render(request, 'order/cancel_order.html', {'order': order})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_transaction_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('transactionId')

        # Припускаючи, що ви збережете номер у полі `card_number` вашої моделі
        # Необхідно адаптувати наступний рядок залежно від вашої моделі та потреб
        order = Order.objects.create(card_number=transaction_id)  # Тут вам потрібно знати, яке замовлення оновлювати

        return JsonResponse({'status': 'success', 'transaction_id': transaction_id})
    else:
        return JsonResponse({'status': 'error'}, status=400)
