from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import PurchaseForm
from users.models import Profile
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required
def create_order(request):
    try:
        cart_items = request.user.cart.cartitem_set.all()
    except AttributeError:
        messages.warning(request, 'Кошик користувача не знайдено.')
        return redirect('cart:cart-view')

    profile = request.user.profile

    if request.method == 'POST':
        form = PurchaseForm(request.POST, initial={'contact': profile.contact, 'firstName': profile.firstName,
                                                   'lastName': profile.lastName, 'address': profile.address})
        if form.is_valid():
            user_profile = Profile.objects.get(user=request.user)
            if user_profile.address and user_profile.contact and user_profile.firstName and user_profile.lastName and user_profile.image:
                order = Order.objects.create(user=request.user, total_price=0)
                total_price = 0

                for cart_item in cart_items:
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price * cart_item.quantity
                    )
                    total_price += order_item.price

                order.total_price = total_price
                order.save()

                request.user.cart.cartitem_set.all().delete()

                return redirect('order:order-detail', order_id=order.id)
            else:
                messages.warning(request, 'Будь ласка, заповніть всі дані профілю перед створенням замовлення.')
                return redirect('order:create-order')
    else:
        form = PurchaseForm(
            initial={'contact': profile.contact, 'firstName': profile.firstName, 'lastName': profile.lastName,
                     'address': profile.address})

    return render(request, 'order/create_order.html',
                  {'form': form, 'cart_items': cart_items})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})
