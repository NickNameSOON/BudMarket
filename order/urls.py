from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('confirm/', views.order_confirm, name='order-confirm'),
    path('process/', views.process_order, name='process-order'),
    path('detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel-order'),
    path('save-transaction/', views.save_transaction_id, name='save-transaction'),
    path('confirm-buy-now/<int:product_id>/', views.confirm_buy_now, name='confirm-buy-now'),
    path('success/', views.order_success, name='order-success'),
    path('liqpay-callback/', views.liqpay_callback, name='liqpay-callback'),

]
