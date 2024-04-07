# forms.py

from django import forms

class PurchaseForm(forms.Form):
    contact = forms.CharField(label='Контактний номер', max_length=100)
    firstName = forms.CharField(label='Ім\'я', max_length=100)
    lastName = forms.CharField(label='Прізвище', max_length=100)
    address = forms.CharField(label='Адреса', max_length=200)
