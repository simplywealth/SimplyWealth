import requests
import os
import logging
import sys 
import pymysql
from datetime import datetime
import uuid
pymysql.version_info = (1, 4, 6, 'final', 0)
pymysql.install_as_MySQLdb()


class LeaderBoard:
    def __init__(self) -> None:
        self.host = 'simplywealth-dev.cja3drzord7s.us-east-1.rds.amazonaws.com'
        self.username = 'python-backend'
        self.password = 'thisisthepassword'
        self.database= 'simplywealth'
        self.API_KEY= "THYPFDH0SM8R242R"


    def get_users_total(self):
        query = "select * from "

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

    def



# # Create a new instance of MyModel
# new_entry = Leaderboard(current_total='60', userid='cat3')
# new_entry.save()
# new_entry = Leaderboard(current_total='0.01', userid='cat4')
# new_entry.save()
# new_entry = Leaderboard(current_total='3000', userid='catadmin')
# new_entry.save()