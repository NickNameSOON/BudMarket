from django import forms
from users.models import Profile
from .models import Order


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contact', 'firstName', 'lastName', 'address']

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_CHOICES, widget=forms.RadioSelect)



class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash_on_delivery', 'Cash on Delivery'),
        # Додайте інші способи оплати, якщо потрібно
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
