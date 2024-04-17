import mysql.connector

def connect_to_rds(host, username, password, database):
    try:
        # Establish connection to the database
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database)

        if connection.is_connected():
            print("Connected to the MySQL database")
            
            # Perform database operations here
            
            # Example: Execute a query
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print("Database version:", db_version)

            # Close cursor and connection
            cursor.close()
            connection.close()
            print("Connection closed")
            
    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)

# Fill in your RDS credentials here
host = 'simplywealth-dev.cja3drzord7s.us-east-1.rds.amazonaws.com'
username = 'python-backend'
password = 'thisisthepassword'
database= 'simplywealth_app'
# Call the function to connect
connect_to_rds(host, username, password, database)