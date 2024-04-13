from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ethereum_wallet_address = models.CharField(max_length=42, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # User balance for kiosk transactions
    pin_hash = models.CharField(max_length=128, default='default_value')

    def __str__(self):
        return self.user.username

    def set_pin(self, pin):
        self.pin_hash = make_password(pin)
        self.save()

    def check_pin(self, pin):
        return check_password(pin, self.pin_hash)

    # need to add methods for user actions


class CardData(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    text = models.TextField()

    def __str__(self):
        return str(self.id)
