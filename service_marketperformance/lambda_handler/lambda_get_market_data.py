
import requests
import os
import logging
import sys 
import pymysql
from datetime import datetime
import uuid
import json
pymysql.version_info = (1, 4, 6, 'final', 0)
pymysql.install_as_MySQLdb()


class MarketStocksDetails:
    def __init__(self) -> None:
        self.host = 'simplywealth-dev.cja3drzord7s.us-east-1.rds.amazonaws.com'
        self.username = 'python-backend'
        self.password = 'thisisthepassword'
        self.database= 'simplywealth'
        self.API_KEY= "THYPFDH0SM8R242R"

    def _create_insert_to_mysql(self,cursor, table_name, data):
        placeholders = ', '.join(['%s'] * len(data[0]))
        columns = ', '.join(data[0].keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = [tuple(item.values()) for item in data]
        cursor.executemany(query, values)


    def update_mysql_rds(self, data):
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database)

            with connection.cursor() as cursor:
                print("Connected to the MySQL database")
                cursor = connection.cursor()
                self._create_insert_to_mysql(cursor, 'SimplyWealthApp_topdailygainers', data[0])
                self._create_insert_to_mysql(cursor, 'SimplyWealthApp_mostactivelytraded', data[1])
                self._create_insert_to_mysql(cursor, 'SimplyWealthApp_topdailylosers', data[2])
            connection.commit()
            print("Changes committed to the database")

        except pymysql.Error as insert_error:
            print("Error inserting data:", insert_error)
            connection.rollback()

        finally:
            cursor.close()
            connection.close()
            print("Connection closed")

    def get_daily_stat(self):
        """only store first 5 """

        url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={self.API_KEY}'
        results = requests.get(url)
        all_data = results.json()

        top_gainers = []
        most_actively_traded = []
        top_losers = []

        try:
            for gainer_data in all_data.get('top_gainers')[:5]:
                gainer = {
                    'unique_key': str(uuid.uuid4()),
                    'insert_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'date': str(datetime.utcnow().date()),
                    'ticker': gainer_data.get('ticker'),
                    'price': gainer_data.get('price'),
                    'change_percentage': float(gainer_data.get('change_percentage').rstrip("%")) / 100,
                    'volume': gainer_data.get('volume')
                }
                top_gainers.append(gainer)

            for active_data in all_data.get('most_actively_traded')[:5]:
                most_active = {
                    'unique_key': str(uuid.uuid4()),
                    'insert_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'date': str(datetime.utcnow().date()),
                    'ticker': active_data.get('ticker'),
                    'price': active_data.get('price'),
                    'change_percentage': float(active_data.get('change_percentage').rstrip("%")) / 100,
                    'volume': active_data.get('volume')
                }
                most_actively_traded.append(most_active)

            for loser_data in all_data.get('top_losers')[:5]:
                loser = {
                    'unique_key': str(uuid.uuid4()),
                    'insert_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'date': str(datetime.utcnow().date()),
                    'ticker': loser_data.get('ticker'),
                    'price': loser_data.get('price'),
                    'change_percentage': float(loser_data.get('change_percentage').rstrip("%")) / 100,
                    'volume': loser_data.get('volume')
                }
                top_losers.append(loser)

            return (top_gainers, most_actively_traded, top_losers)
        except Exception as err: 
            logging.exception(err)
            sys.exit(1)

    def start_process(self):
        results = self.get_daily_stat()
        self.update_mysql_rds(results)




# Call the function to connect
