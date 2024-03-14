from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

'''class NewUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "focus:outline-none", "placeholder": "mail@mail.com"}
        ),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "focus:outline-none", "placeholder": "Enter username..."}
        ),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "focus:outline-none", "placeholder": "Enter password"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "focus:outline-none", "placeholder": "Enter same password"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
'''
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class = shadow appearance-none border rounded py-2 px-3 mr-10 text-gray-700 leading-tight": "focus:outline-none", "placeholder": "Enter username..."}
        ))

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class = shadow appearance-none border rounded py-2 px-3 mr-10 text-gray-700 leading-tight": "focus:outline-none", "placeholder": "mail@mail.com"}
        ))

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class = shadow appearance-none border rounded py-2 px-3 mr-10 text-gray-700 leading-tight": "focus:outline-none", "placeholder": "Enter password"}
        ))
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class = shadow appearance-none border rounded py-2 px-3 mr-10 text-gray-700 leading-tight": "focus:outline-none", "placeholder": "Enter same password"}
        ))

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
