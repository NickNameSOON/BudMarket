# admin_panel/forms.py
from django import forms

class UserSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Пошук', widget=forms.TextInput(attrs={'placeholder': 'Пошук за ім\'ям, прізвищем, номером телефону або email', 'class': "mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm px-4 py-2"}))
