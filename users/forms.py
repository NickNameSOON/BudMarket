from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

User = get_user_model()


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                            'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                           'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                                 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                                 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'contact', 'firstName', 'lastName', 'address']
        labels = {
            'image': 'Фото профілю',
            'contact': 'Контактний номер',
            'firstName': "Ім'я",
            'lastName': 'Прізвище',
            'address': 'Адреса'
        }
