from django.forms import ModelForm, ChoiceField
from .models import Location
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LocationEdit(ModelForm):
    location_type = ChoiceField(choices=Location.TYPE_CHOICES)

    class Meta:
        model = Location
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
