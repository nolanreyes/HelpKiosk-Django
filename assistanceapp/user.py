from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = None  # not needed
    email = None  # not needed either
    wallet_address = models.CharField(max_length=42, unique=True, primary_key=True,
                                      help_text=_("Ethereum wallet address"))

    USERNAME_FIELD = 'wallet_address'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.wallet_address
