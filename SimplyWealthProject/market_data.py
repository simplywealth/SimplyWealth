import requests
import os
import django 
import uuid 
import logging 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyWealthProject.settings")
django.setup()

from SimplyWealthApp.models import TopDailyGainers, TopDailyLosers, MostActivelyTraded
from django.utils import timezone

API_KEY= "THYPFDH0SM8R242R"

def get_daily_stat():
    """Service to Populate the Marketperformance Stats. 
    """

    url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}'
    r = requests.get(url)
    all_data = r.json()

    for gainer_data in all_data.get('top_gainers')[:5]:
        gainer = TopDailyGainers(
            unique_key = uuid.uuid4().hex,
            date=timezone.now().date(),
            ticker=gainer_data.get('ticker'), 
            price=gainer_data.get('price'), 
            change_percentage=float(gainer_data.get('change_percentage').rstrip("%"))/100, 
            volume=gainer_data.get('volume')
        )
        logging.info(gainer)
        gainer.save()

    for active_data in all_data.get('most_actively_traded')[:5]:
        most_active = MostActivelyTraded(
            unique_key = uuid.uuid4().hex,
            date=timezone.now().date(),
            ticker=active_data.get('ticker'), 
            price=active_data.get('price'), 
            change_percentage=float(active_data.get('change_percentage').rstrip("%"))/100, 
            volume=active_data.get('volume')
        )
        logging.info(most_active)
        most_active.save()

    for loser_data in all_data.get('top_losers')[:5]:
        loser = TopDailyLosers(
            unique_key = uuid.uuid4().hex,
            date=timezone.now().date(),
            ticker=loser_data.get('ticker'), 
            price=loser_data.get('price'), 
            change_percentage=float(loser_data.get('change_percentage').rstrip("%"))/100, 
            volume=loser_data.get('volume')
        )
        logging.info(loser)
        loser.save()
        

get_daily_stat()