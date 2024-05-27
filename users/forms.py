from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contactNumber', 'firstName', 'email', 'lastName', 'DeliveryAddress']
        labels = {
            'contactNumber': 'Контактний номер',
            'firstName': "Ім'я",
            'lastName': 'Прізвище',
            'DeliveryAddress': 'Адреса Доставки',
            'email': 'Електронна пошта'
        }



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старий пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': '************', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}),
    )
    new_password1 = forms.CharField(
        label="Новий пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': '************', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}),
    )
    new_password2 = forms.CharField(
        label="Підтвердіть новий пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': '************', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}),
    )
