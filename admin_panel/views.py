from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from order.models import Order
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_staff or user.groups.filter(name='Admin').exists()


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'dashboard.html')


@staff_member_required
def order_list(request):
    orders = Order.objects.all()

    # Сортування за датою
    sort = request.GET.get('sort', 'desc')
    if sort == 'asc':
        orders = orders.order_by('created_at')
    else:
        orders = orders.order_by('-created_at')

    # Пошук за користувачем
    username = request.GET.get('username')
    if username:
        orders = orders.filter(user__username__icontains=username)

    # Пошук за ID замовлення
    order_id = request.GET.get('order_id')
    if order_id:
        orders = orders.filter(id=order_id)

    return render(request, 'orders.html', {'orders': orders, 'sort': sort})


# admin_panel/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from users.models import Profile
from .forms import UserSearchForm


@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    form = UserSearchForm(request.GET or None)
    users = Profile.objects.all().select_related('user')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            users = users.filter(
                Q(firstName__icontains=query) |
                Q(lastName__icontains=query) |
                Q(contactNumber__icontains=query) |
                Q(email__icontains=query)
            )

    sort_by = request.GET.get('sort', 'id')
    if sort_by == 'purchase_time':
        users = users.order_by('-user__date_joined')
    else:
        users = users.order_by(sort_by)

    context = {
        'users': users,
        'form': form,
    }
    return render(request, 'users.html', context)


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
        return redirect('admin_panel:order-list')  # Припускаємо, що є сторінка зі списком замовлень

    return render(request, 'order_detail.html', {'order': order})
