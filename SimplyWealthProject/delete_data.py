import requests
import os 
import django 
import json
import datetime as dt
import logging
import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyWealthProject.settings")
django.setup()


from SimplyWealthApp.models import  Leaderboard

Leaderboard.objects.all().delete()


# Create a new instance of MyModel
new_entry = Leaderboard(current_total='-5%', userid='cat3')
new_entry.save()
new_entry = Leaderboard(current_total='+0.01%', userid='cat4')
new_entry.save()
new_entry = Leaderboard(current_total='+300%', userid='catadmin')
new_entry.save()