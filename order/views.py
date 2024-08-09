import json
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
from liqpay import LiqPay
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
        comment = request.POST.get('comment')
        delivery_method = request.POST.get('delivery_method')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')

        if payment_method not in ['cash', 'liqpay']:
            messages.error(request, "Невідомий метод оплати.")
            return redirect('cart:cart-view')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                delivery_address=delivery_address,
                delivery_method=delivery_method,
                payment_method=payment_method,
                comment=comment,
                first_name=first_name,
                last_name=last_name,
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

            send_order_confirmation_email(order)  # Відправка електронного листа

            if payment_method == 'liqpay':
                liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
                params = {
                    'action': 'pay',
                    'amount': str(order.total_price),
                    'currency': 'UAH',
                    'description': 'Payment for order #{}'.format(order.id),
                    'order_id': str(order.id),
                    'version': '3',
                    'sandbox': 1,  # 1 - sandbox mode, 0 - live mode
                    'server_url': request.build_absolute_uri(reverse('order:liqpay-callback')),
                    'result_url': request.build_absolute_uri(reverse('order:order-success')),
                }
                payment_data = liqpay.cnb_form(params)
                return JsonResponse({'payment_data': payment_data})
            else:
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
    product = get_object_or_404(Product, id=product_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        contact_number = request.POST.get('contactNumber')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        delivery_method = request.POST.get('delivery_method')
        delivery_address = request.POST.get('delivery_address')
        payment_method = request.POST.get('paymentMethod')
        comment = request.POST.get('comment')

        if payment_method not in ['cash', 'liqpay']:
            messages.error(request, "Невідомий метод оплати.")
            return redirect('cart:cart-view')

        with transaction.atomic():
            try:
                order = Order.objects.create(
                    user=request.user,
                    delivery_address=delivery_address if delivery_method == 'delivery' else 'Самовивіз',
                    delivery_method=delivery_method,
                    payment_method=payment_method,
                    contact_number=contact_number,
                    first_name=first_name,
                    last_name=last_name,
                    comment=comment,
                )

                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=product.price
                )

                order.total_price = order_item.price
                order.save()

                send_order_confirmation_email(order)  # Відправка електронного листа

                if payment_method == 'liqpay':
                    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
                    params = {
                        'action': 'pay',
                        'amount': str(order.total_price),
                        'currency': 'UAH',
                        'description': 'Payment for order #{}'.format(order.id),
                        'order_id': str(order.id),
                        'version': '3',
                        'sandbox': 1,  # 1 - sandbox mode, 0 - live mode
                        'server_url': request.build_absolute_uri(reverse('order:liqpay-callback')),
                        'result_url': request.build_absolute_uri(reverse('order:order-success')),
                    }
                    payment_data = liqpay.cnb_form(params)
                    return JsonResponse({'payment_data': payment_data})
                else:
                    messages.success(request, "Ваше замовлення було успішно створене.")
                    return redirect('order:order-success')

            except Exception as e:
                messages.error(request, f"Сталася помилка під час обробки вашого замовлення: {str(e)}")
                return redirect('cart:cart-view')
    else:
        context = {
            'product': product,
            'profile': profile,
        }
        return render(request, 'order/confirm_buy_now.html', context)


@login_required
def order_success(request):
    return render(request, 'order/success.html')


@csrf_exempt
def liqpay_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        transaction_id = data.get('transaction_id')
        status = data.get('status')

        order = get_object_or_404(Order, id=order_id)

        if status == 'success':
            order.paid = True
            order.payment_id = transaction_id
            order.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Payment not successful'}, status=400)

    return JsonResponse({'status': 'error'}, status=400)


def send_order_confirmation_email(order):
    subject = f'Підтвердження замовлення #{order.id}'
    html_message = render_to_string('email/order_confirmation_email.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
