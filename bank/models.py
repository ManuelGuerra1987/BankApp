from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    usd_account = models.DecimalField(decimal_places=2, max_digits=16, default=0)
    eur_account = models.DecimalField(decimal_places=2, max_digits=16, default=0)
    account_number = models.CharField(max_length=12, unique=True)
