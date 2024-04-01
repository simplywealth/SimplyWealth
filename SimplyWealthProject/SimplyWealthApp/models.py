from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Stocks(models.Model):
    tick_symbol=models.CharField(max_length=5)
    market_value=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tick_symbol}-{self.market_value}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank = True, null=True)
    text= models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

class StockTransanctions(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    transaction_id = models.CharField(primary_key= True, max_length=100, unique=True)
    stock_symbol = models.CharField(max_length=5)
    transaction_type = models.CharField(max_length=4, default='buy')
    stock_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_units = models.DecimalField(max_digits=10, decimal_places=2)
    stock_price_date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)

class UserStockPortfolio(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=5)
    stock_units = models.DecimalField(max_digits=10, decimal_places=2)   
        



class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    transaction_id = models.CharField(primary_key= True, max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.user.user.username}, Amount: {self.amount}, Timestamp: {self.timestamp}"