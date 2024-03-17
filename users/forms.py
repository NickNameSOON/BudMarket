from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email' , 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    password = forms.CharField(required= True, widget=forms.PasswordInput(attrs={'placeholder': 'Password' , 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password": {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'], None, validated_data['password'])

            return user
