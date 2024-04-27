# from django.contrib.auth.models import User
# from SimplyWealthApp.models import UserProfile
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyWealthProject.settings")
django.setup()

# Importing all models
from django.contrib.auth.models import User
from SimplyWealthApp.models import UserProfile, Transaction, StockTransanctions, UserStockPortfolio, StocksPriceHistory, Leaderboard, TopDailyGainers, MostActivelyTraded, TopDailyLosers

# Deleting data from all models
# Start from models that do not have foreign keys from other models
StocksPriceHistory.objects.all().delete()
Leaderboard.objects.all().delete()
TopDailyGainers.objects.all().delete()
MostActivelyTraded.objects.all().delete()
TopDailyLosers.objects.all().delete()

# Then delete from models that have foreign keys pointing to the UserProfile
StockTransanctions.objects.all().delete()
UserStockPortfolio.objects.all().delete()
Transaction.objects.all().delete()

# Finally, delete from the UserProfile and User models
UserProfile.objects.all().delete()  # This will cascade and delete associated Users automatically if UserProfile is the primary user model and User is referenced with on_delete=CASCADE

# If UserProfile is not set as the primary user model (i.e., just a related model to User),
# or if you want to be explicit about deleting Users last
User.objects.all().delete()
