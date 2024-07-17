# forms.py
from django import forms
from .models import HomeImage


class HomeImageAdminForm(forms.ModelForm):
    class Meta:
        model = HomeImage
        fields = ['image', 'alt', 'order', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget = forms.TextInput(attrs={'list': 'url-list'})
