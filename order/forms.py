from django import forms
from users.models import Profile
from .models import Order

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contactNumber', 'firstName', 'lastName', 'DeliveryAddress']

class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        # Додайте інші способи оплати, якщо потрібно
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

class DeliveryForm(forms.Form):
    DELIVERY_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    ]
    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect)
    delivery_address = forms.CharField(required=False)  # Задайте required=False для гнучкості

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')
        delivery_address = cleaned_data.get('delivery_address')

        if delivery_method == 'delivery' and not delivery_address:
            raise forms.ValidationError("Please enter a delivery address for delivery option.")

        return cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method', 'delivery_method', 'delivery_address', 'payment_intent_id']
