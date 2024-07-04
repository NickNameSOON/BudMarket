import json
import hashlib
import requests
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from market.models import Product
from .models import Order, OrderItem
from cart.models import CartItem, Cart
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from users.models import Profile
import logging


logger = logging.getLogger(__name__)

@login_required
def process_order(request):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            messages.error(request, "Кошик не знайдено.")
            return redirect('cart:cart-view')

        delivery_address = request.POST.get('delivery_address')
        payment_method = request.POST.get('paymentMethod')

        if payment_method not in ['cash', 'wayforpay']:
            messages.error(request, "Невідомий метод оплати.")
            return redirect('cart:cart-view')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                delivery_address=delivery_address,
                payment_method=payment_method
            )

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

            cart.cartitem_set.all().delete()

            if payment_method == 'cart':
                payment_data = {
                    'orderReference': str(order.id),
                    'merchantAccount': settings.WAYFORPAY_MERCHANT_ACCOUNT,
                    'orderDate': int(order.created_at.timestamp()),
                    'amount': float(order.total_price),
                    'currency': 'UAH',
                    'productName': [item.product.title for item in order.orderitem_set.all()],
                    'productPrice': [float(item.price) for item in order.orderitem_set.all()],
                    'productCount': [item.quantity for item in order.orderitem_set.all()],
                    'merchantSignature': hashlib.sha256(
                        (settings.WAYFORPAY_MERCHANT_ACCOUNT +
                         str(order.id) +
                         str(int(order.created_at.timestamp())) +
                         str(float(order.total_price)) +
                         'UAH' +
                         ''.join([item.product.name for item in order.orderitem_set.all()]) +
                         ''.join([str(float(item.price)) for item in order.orderitem_set.all()]) +
                         ''.join([str(item.quantity) for item in order.orderitem_set.all()]) +
                         settings.WAYFORPAY_SECRET_KEY).encode('utf-8')).hexdigest()
                }
                response = requests.post(settings.WAYFORPAY_API_URL, json=payment_data)
                payment_response = response.json()

                if payment_response['reasonCode'] == 1100:
                    return JsonResponse({'invoiceUrl': payment_response['invoiceUrl']})
                else:
                    messages.error(request, "Помилка при обробці платежу WayForPay.")
                    return redirect('cart:cart-view')
            else:
                order.save()
                messages.success(request, "Ваше замовлення було успішно створене.")
                return redirect('order:order-success')
    else:
        return redirect('cart:cart-view')


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this order.")
    return render(request, 'order/order_detail.html', {'order': order})


def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.status = Order.CANCELED
        order.save()
        messages.info(request, "Замовлення скасовано.")
        return redirect('order:order-detail', order_id=order_id)
    return render(request, 'order/cancel_order.html', {'order': order})


@csrf_exempt
def save_transaction_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('transactionId')
        order = Order.objects.filter(id=transaction_id).first()
        if order:
            order.payment_id = transaction_id
            order.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction_id})
        return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)


def order_confirm(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        messages.error(request, "Кошик порожній.")
        return redirect('cart:cart-view')

    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'order/confirmation.html', context)


@login_required
def confirm_buy_now(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        contactNumber = request.POST.get('contactNumber')
        email = request.POST.get('email')
        payment_method = request.POST.get('paymentMethod')
        delivery_method = request.POST.get('delivery_method')
        delivery_address = request.POST.get('delivery_address', '')

        if payment_method not in ['creditCard', 'cash']:
            messages.error(request, "Невідомий метод оплати.")
            return redirect('order:confirm-buy-now', product_id=product_id)

        if not (firstName and lastName and contactNumber and email):
            messages.error(request, "Будь ласка, заповніть усі обов’язкові поля.")
            return redirect('order:confirm-buy-now', product_id=product_id)

        order = Order.objects.create(
            user=request.user,
            delivery_method=delivery_method,
            payment_method=payment_method,
            delivery_address=delivery_address,
            total_price=product.price
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )

        if payment_method == 'cart':
            payment_data = {
                'orderReference': str(order.id),
                'merchantAccount': settings.WAYFORPAY_MERCHANT_ACCOUNT,
                'orderDate': int(order.created_at.timestamp()),
                'amount': float(order.total_price),
                'currency': 'UAH',
                'productName': [product.title],
                'productPrice': [float(product.price)],
                'productCount': [1],
                'merchantSignature': hashlib.sha256(
                    (settings.WAYFORPAY_MERCHANT_ACCOUNT +
                     str(order.id) +
                     str(int(order.created_at.timestamp())) +
                     str(float(order.total_price)) +
                     'UAH' +
                     product.name +
                     str(float(product.price)) +
                     '1' +
                     settings.WAYFORPAY_SECRET_KEY).encode('utf-8')).hexdigest()
            }
            response = requests.post(settings.WAYFORPAY_API_URL, json=payment_data)
            payment_response = response.json()

            if payment_response['reasonCode'] == 1100:
                return JsonResponse({'invoiceUrl': payment_response['invoiceUrl']})
            else:
                messages.error(request, "Помилка при обробці платежу WayForPay.")
                return redirect('order:confirm-buy-now', product_id=product_id)

        order.save()
        messages.success(request, "Ваше замовлення було успішно створене.")
        return redirect('order:order-success')

    context = {
        'product': product,
        'profile': profile,
    }
    return render(request, 'order/confirm_buy_now.html', context)


@login_required
def order_success(request):
    return render(request, 'order/success.html')


@csrf_exempt
def wayforpay_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_reference = data.get('orderReference')
        order = get_object_or_404(Order, id=order_reference)

        if data.get('transactionStatus') == 'Approved':
            order.paid = True
            order.save()
            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Payment not approved'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

