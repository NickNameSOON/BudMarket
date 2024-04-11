from django import forms
from .models import CartItem
from users.models import Profile

class CartAddProductForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['quantity']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'email', 'image', 'contact', 'firstName', 'lastName', 'address']
