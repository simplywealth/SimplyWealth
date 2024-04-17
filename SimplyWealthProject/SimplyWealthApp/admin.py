from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(StockTransanctions)
admin.site.register(UserStockPortfolio)
admin.site.register(StocksPriceHistory)
admin.site.register(Leaderboard)