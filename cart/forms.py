from django import forms
from .models import CartItem

class CartAddProductForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['quantity']
