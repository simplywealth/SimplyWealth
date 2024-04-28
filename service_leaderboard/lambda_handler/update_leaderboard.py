import requests
import os
import logging
import sys 
import pymysql
from datetime import datetime
import uuid
import pandas as pd
import json
pymysql.version_info = (1, 4, 6, 'final', 0)
pymysql.install_as_MySQLdb()

# USER_TOTAL_WORTH = current_total$ + (stock_price * stock_unit)
# ranking - order USER_TOTAL_WORTH 
# insert top 5 into this week's leaderboard table 


class LeaderBoard:

    def __init__(self) -> None:
        self.host = 'simplywealth-dev.cja3drzord7s.us-east-1.rds.amazonaws.com'
        self.username = 'python-backend'
        self.password = 'thisisthepassword'
        self.database= 'simplywealth'
        self.API_KEY= "THYPFDH0SM8R242R"
        self.connection = self._get_db_connection()
        print("Established DB connection")

    def _get_db_connection(self):
        connection = pymysql.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database)
        return connection

    def main(self):
        portfolio_df = self.get_transactions()
        user_networth = self.calculate_net_worth(portfolio_df=portfolio_df)
        self.update_leaderboard_table(user_networth=user_networth)


    def _get_stock_prices(self, stock_symbols):
        """ get the price of stocks
        """
        stocks_current_prices ={}
        for symbol in stock_symbols:
            ticker_details_endpoint_url= f"https://api.polygon.io/v3/reference/tickers?search={symbol}&active=true&limit=5&apiKey=UqR1AwHB4eIRO0pUzjG8IxuMlFHeJczI"
            response = requests.get(ticker_details_endpoint_url).json()
            output_response = {'results':json.dumps(response['results'])}
            stocks_current_prices[symbol]=output_response.get('price')

        return stocks_current_prices


    def get_transactions(self):
        """query db and get unique purchased stocks.
        find their current prices
        calculate user total in stock portfolio
        """
        query = "select * from SimplyWealthApp_userstockportfolio;"
        try:
            df= pd.read_sql(query, self.connection)

            stock_symbols = set(df['stock_symbol'])
            stocks_current_prices = self._get_stock_prices(stock_symbols)

            stock_worth = []
            for _, transaction in df.iterrows():
                stock_worth.append(transaction['stock_units'] * stocks_current_prices.get(transaction['stock_symbol']))

            df['stock_worth'] = stock_worth
            self.connection.close()

        except pymysql.Error as insert_error:
            print("Error inserting data:", insert_error)
            self.connection.rollback()

        finally:
            self.connection.close()
            print("Connection closed")

        return df

    def calculate_net_worth(self, portfolio_df):

        ### get how much $$ user have in bank. (aka have not spent)
        query_file = os.path.join(os.path.dirname(__file__), "query_latest_in_bank.sql")
        with open(query_file, 'r') as f:
            query = f.readlines()

        transaction_df= pd.read_sql(query, self.connection)

        # get total $$ in user's portfolio
        portfolio_df.groupby('user_id').sum()[['stock_worth']]

        #calculate user's net worth
        combined_df = transaction_df[['user_id', 'amount']].merge(portfolio_df[['user_id', 'stock_worth']], how='left', left_on='user_id', right_on='user_id')
        combined_df['total'] = combined_df['amount'] + combined_df['stock_worth']

        return combined_df[['total', 'stock_worth']]



    def update_leaderboard_table(self, df):
        """ Filter on top 5. Insert into LeaderBoard DB
        """
        query = "insert into SimplyWealthApp_leaderboard_weekly (currenttime, userid, current_total) values (current_date(), %, %);"
 
        data = df.sort_values(by ='stock_worth', ascending=False).head(5)

        values = [tuple(row) for row in data.values]

        try:
            with self.connection.cursor() as cursor:
                print("Connected to the MySQL database")
                cursor.executemany(query, values)

        except pymysql.Error as insert_error:
            print("Error inserting data:", insert_error)
            self.connection.rollback()

        finally:
            cursor.close()
            self.connection.close()
            print("Connection closed")


# LeaderBoard().main()