import os
import requests
import json
import mysql.connector
from dotenv import load_dotenv
class Probate:
    def __init__(self):
        load_dotenv()
        self.connection = mysql.connector.connect(
            host= os.getenv("DB_HOST"),
            user= os.getenv("DB_USERNAME"),
            password= os.getenv("DB_PASSWORD"),
            database= os.getenv("DB_DATABASE"),
        )
        self.cursor = self.connection.cursor(dictionary=True)
        self.table_name = os.getenv("DB_TABLE")
        
    def execute_query(self, query, data=None):
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def select(self, conditions=None):
        query = f"SELECT * FROM {self.table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        return self.execute_query(query)

    def select_existing_data(self, data):
        conditions = ' AND '.join([f"{key} = %s" for key in data.keys()])
        query = f"SELECT * FROM {self.table_name} WHERE {conditions}"
        self.execute_query(query, tuple(data.values()))
        result = self.cursor.fetchone()
        return result


    def insert(self, data):
        existing_data = self.select_existing_data(data)
    
        if existing_data:
            # Data with the same key(s) already exists, you can choose to update it or skip the insertion
            print("Data already exists:", existing_data)
            # Add your code here to handle the existing data
        else:
            columns = ', '.join(data.keys())
            values = ', '.join(['%s' for _ in data.values()])
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            self.execute_query(query, tuple(data.values()))
            self.connection.commit()

    def update(self, data, conditions=None):
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause}"
        if conditions:
            query += f" WHERE {conditions}"
        self.execute_query(query, tuple(data.values()))
        self.connection.commit()

    def delete(self, conditions=None):
        query = f"DELETE FROM {self.table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        self.execute_query(query)
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    db = DatabaseConnector()
    for i in range(2,1000):
        data = {
            
        }
        db.insert(data)

    db.close_connection()