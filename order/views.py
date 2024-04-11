from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PurchaseForm, PaymentForm
from .models import Order, OrderItem
from cart.models import CartItem
from django.contrib import messages
from django.db import transaction


@login_required
def order_confirmation(request):
    user_profile = request.user.profile
    cart_items = CartItem.objects.filter(cart__user=request.user)
    purchase_form = PurchaseForm(instance=user_profile)
    payment_form = PaymentForm()

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_method = payment_form.cleaned_data['payment_method']

            if payment_method == 'delivery':
                purchase_form = PurchaseForm(request.POST, instance=user_profile)
                if purchase_form.is_valid():
                    purchase_form.save()
                else:
                    messages.error(request, "Будь ласка, вкажіть адресу доставки.")
                    return render(request, 'order/order_confirmation.html', {
                        'purchase_form': purchase_form,
                        'payment_form': payment_form,
                        'cart_items': cart_items
                    })

            # Створення замовлення
            order = Order.objects.create(
                user=request.user,
                payment_method=payment_method,
                # Додайте інші поля як необхідно
            )

            # Додаємо товари з кошика до замовлення
            order_items = [
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                for cart_item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            # Очищення кошика
            cart_items.delete()

            messages.success(request, "Ваше замовлення успішно оформлене.")
            return redirect('order:order-detail', order_id=order.pk)

    return render(request, 'order/order_confirmation.html', {
        'purchase_form': purchase_form,
        'payment_form': payment_form,
        'cart_items': cart_items
    })



def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.user != request.user:
        # Якщо користувач не є власником замовлення, перенаправляємо його на сторінку заборони
        return HttpResponseForbidden("You don't have permission to view this order.")
    return render(request, 'order/order_detail.html', {'order': order})


def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        # Тут ви можете виконати додаткову логіку, якщо потрібно перед відміною замовлення
        order.status = Order.CANCELED
        order.save()
        return redirect('order:order-detail', order_id=order_id)
    return render(request, 'order/cancel_order.html', {'order': order})
