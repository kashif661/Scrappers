import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connections = {}  # This dictionary will store the database connections and cursors

def update_db_connections(db_name):
    # Assuming you have the necessary details for connecting to the 'ovh2' database
    connection_details = {
        'host': os.getenv("DB_HOST"),
        'user': os.getenv("DB_USERNAME"),
        'password': os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_DATABASE")
    }

    try:
        # Establishing a connection to the MySQL server
        connection = mysql.connector.connect(
            host=connection_details['host'],
            user=connection_details['user'],
            password=connection_details['password'],
            database=connection_details['database']
        )

        cursor = connection.cursor()

        # Store the connection and cursor in the connections dictionary
        connections[db_name] = (connection, cursor)

        #print(f"Successfully connected to the '{db_name}' database.")

    except mysql.connector.Error as e:
        print(f"Error connecting to '{db_name}' database:", e)