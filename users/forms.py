from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

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

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'shadow appearance-none border rounded py-2 px-3 mr-15 text-gray-700 leading-tight focus:outline-none'}))
