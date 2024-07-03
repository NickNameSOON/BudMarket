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
import stripe
from users.models import Profile
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def process_order(request):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            messages.error(request, "Кошик не знайдено.")
            return redirect('cart:cart-view')

        logger.info('Cart found: %s', cart)

        delivery_address = request.POST.get('delivery_address')
        payment_method = request.POST.get('paymentMethod')

        if payment_method not in ['stripe', 'cash']:
            messages.error(request, "Невідомий метод оплати.")
            return redirect('cart:cart-view')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                delivery_address=delivery_address,
                payment_method=payment_method
            )
            logger.info('Order created: %s', order)

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
            logger.info('Order updated with total price: %s', total_price)

            cart.cartitem_set.all().delete()

            if payment_method == 'stripe':
                intent = stripe.PaymentIntent.create(
                    amount=int(order.total_price * 100),  # Сума в копійках
                    currency='uah',
                    metadata={'order_id': order.id}
                )
                order.payment_intent_id = intent['id']
                order.save()
                logger.info('Stripe PaymentIntent created: %s', intent['id'])
                return JsonResponse({'client_secret': intent['client_secret']})
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

        if payment_method == 'creditCard':
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),
                currency='uah',
                metadata={'order_id': order.id}
            )
            order.payment_intent_id = intent['id']
            order.save()
            return JsonResponse({'client_secret': intent['client_secret']})

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
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata']['order_id']
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()

    return HttpResponse(status=200)
