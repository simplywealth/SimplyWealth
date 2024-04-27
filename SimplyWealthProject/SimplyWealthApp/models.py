from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


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
    def __str__(self):
        return f"Stock Transaction for {self.user.user.username}, Stock: {self.stock_symbol}, Stock Units: {self.stock_units}, Transaction Type: {self.transaction_type}, Timestamp: {self.timestamp}"

class UserStockPortfolio(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=5)
    stock_units = models.DecimalField(max_digits=10, decimal_places=2) 
    def __str__(self):
        return f"User Stock Portfolio: {self.user.user.username}, Stock: {self.stock_symbol}, Stock Units: {self.stock_units}"
  
    
class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    transaction_id = models.CharField(primary_key= True, max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.user.user.username}, Amount: {self.amount}, Timestamp: {self.timestamp}"



class StocksPriceHistory(models.Model):
    unique_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_time = models.DateField(auto_now_add=True) #automatically fill in with current datetime
    stock_name = models.CharField(max_length=50)
    ticker=models.CharField(max_length=10)
    price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.current_time}--{self.tick_symbol}-{self.market_value}"


class Leaderboard_Weekly(models.Model):
    currenttime = models.DateField(auto_now_add=True) 
    userid = models.CharField(max_length=30)
    current_total=models.DecimalField(max_digits=10, decimal_places=2)


class TopDailyGainers(models.Model):
    unique_key = models.CharField(primary_key=True, max_length=36)  # Use CharField instead of UUIDField
    insert_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    ticker = models.CharField(max_length=20)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    change_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    volume = models.DecimalField(max_digits=15, decimal_places=2) 


class MostActivelyTraded(models.Model):
    unique_key = models.CharField(primary_key=True, max_length=36)  # Use CharField instead of UUIDField
    insert_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    ticker = models.CharField(max_length=20)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    change_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    volume = models.DecimalField(max_digits=15, decimal_places=2) 


class TopDailyLosers(models.Model):
    unique_key = models.CharField(primary_key=True, max_length=36)  # Use CharField instead of UUIDField
    insert_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    ticker = models.CharField(max_length=20)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    change_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    volume = models.DecimalField(max_digits=15, decimal_places=2) 