import requests
import os 
import django 
import json
import datetime as dt
import logging
import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyWealthProject.settings")
django.setup()


from SimplyWealthApp.models import UserStockPortfolio, Leaderboard

class CurrentStockPrices:
        
    def get_distinct_stocks(self):
        tickers=[]
        stock_portfolios = UserStockPortfolio.objects.all()
        for portfolio in stock_portfolios:
            tickers.append(portfolio.stock_symbol)

        return set(tickers)


    def get_current_price(self, stock_name):
        """
        https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date
        """
        # try:
        yester_date = (dt.datetime.now().date() - dt.timedelta(days=3)).strftime('%Y-%m-%d')
        current_price_url = f"https://api.polygon.io/v1/open-close/{stock_name}/{yester_date}?adjusted=true&apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE"
        response = requests.get(current_price_url).json()   
        latest_close_prices = response.get('close')
        print(f"latest close prices for {stock_name}, {latest_close_prices}")
        # except Exception as err:
        #     logging.info(err)
        #     time.sleep(5 * 60)
        #     self.get_current_price(stock_name)

        ### add to leaderboard table
        Leaderboard_record = Leaderboard.objects.create(stock_name=stock_name, price=latest_close_prices)
        Leaderboard_record.save()

def main():
    csp = CurrentStockPrices()
    print(csp)
    stocks = csp.get_distinct_stocks()
    print(stocks)
    # for s in stocks:
    #     csp.get_current_price(s)