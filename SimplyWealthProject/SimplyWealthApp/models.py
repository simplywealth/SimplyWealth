from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Stocks(models.Model):
    tick_symbol=models.CharField(max_length=5)
    market_value=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tick_symbol}-{self.market_value}"


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank = True, null=True)
    text= models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username