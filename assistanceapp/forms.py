from django.forms import ModelForm
from django import forms
from .models import Location
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LocationEdit(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']