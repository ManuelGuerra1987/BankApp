from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    usd_account = models.DecimalField(decimal_places=2, max_digits=16, default=0)
    eur_account = models.DecimalField(decimal_places=2, max_digits=16, default=0)
    account_number = models.CharField(max_length=12, unique=True)

class StockPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    stock_symbol = models.CharField(max_length=10)  
    quantity = models.PositiveIntegerField(default=0)  
    purchase_price = models.DecimalField(decimal_places=2, max_digits=16)  
    date_acquired = models.DateField(auto_now_add=True)     
