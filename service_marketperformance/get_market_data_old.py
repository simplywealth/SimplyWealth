import requests
import os
import django 
import logging
import sys 

sys.path.append('/Users/sk_courseworks/Course_Work/cs673/PROJECT_PHASE2/SimplyWealth/SimplyWealthProject')
os.chdir('/Users/sk_courseworks/Course_Work/cs673/PROJECT_PHASE2/SimplyWealth/SimplyWealthProject')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyWealthProject.settings")
django.setup()

from SimplyWealthApp.models import TopDailyGainers, TopDailyLosers, MostActivelyTraded
from django.utils import timezone

API_KEY= "THYPFDH0SM8R242R"

def get_daily_stat():
    """only store first 5 """

    url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}'
    results = requests.get(url)
    all_data = results.json()

    try:
        for gainer_data in all_data.get('top_gainers')[:5]:
            gainer = TopDailyGainers(
                date=timezone.now().date(),
                ticker=gainer_data.get('ticker'), 
                price=gainer_data.get('price'), 
                change_percentage=float(gainer_data.get('change_percentage').rstrip("%"))/100, 
                volume=gainer_data.get('volume')
            )
            gainer.save()
            print('Inserted Top 5 market performing stocks of the day')

        for active_data in all_data.get('most_actively_traded')[:5]:
            most_active = MostActivelyTraded(
                date=timezone.now().date(),
                ticker=active_data.get('ticker'), 
                price=active_data.get('price'), 
                change_percentage=float(active_data.get('change_percentage').rstrip("%"))/100, 
                volume=active_data.get('volume')
            )
            print('Inserted Top 5 Actively Trading stocks of the day')
            most_active.save()

        for loser_data in all_data.get('top_losers')[:5]:
            loser = TopDailyLosers(
                date=timezone.now().date(),
                ticker=loser_data.get('ticker'), 
                price=loser_data.get('price'), 
                change_percentage=float(loser_data.get('change_percentage').rstrip("%"))/100, 
                volume=loser_data.get('volume')
            )
            print('Inserted Top 5 Actively Trading stocks of the day ')
            loser.save()

    except Exception as err: 
        logging.exception(err)
        sys.exit(1)

get_daily_stat()