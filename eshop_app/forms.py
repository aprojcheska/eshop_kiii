from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser

        exclude = ['user', ]
        fields = ['first_name', 'last_name', 'phone', 'city', 'street', 'street_no']


class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo']



