# db_manager.py

import pymongo
import psycopg2
import mysql.connector
from sqlalchemy import create_engine


class DBManager:
    def __init__(
        self, db_type, db_name, host="localhost", port=None, user=None, password=None
    ):
        self.db_type = db_type.lower()
        self.db_name = db_name
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        if self.db_type == "mongo":
            self.client = pymongo.MongoClient(host, port)
            self.db = self.client[db_name]
        elif self.db_type == "postgres":
            self.conn = psycopg2.connect(
                dbname=db_name, user=user, password=password, host=host, port=port
            )
            self.cursor = self.conn.cursor()
        elif self.db_type == "mysql":
            self.conn = mysql.connector.connect(
                host=host, user=user, password=password, database=db_name, port=port
            )
            self.cursor = self.conn.cursor(dictionary=True)
        else:
            raise ValueError("Unsupported database type")

    def get_collection(self, collection_name):
        if self.db_type == "mongo":
            return self.db[collection_name]
        else:
            raise ValueError("get_collection is only supported for MongoDB")

    def execute_query(self, query, params=None):
        if self.db_type in ["postgres", "mysql"]:
            self.cursor.execute(query, params)
            self.conn.commit()
        else:
            raise ValueError("execute_query is only supported for SQL databases")

    def fetch_results(self):
        if self.db_type in ["postgres", "mysql"]:
            return self.cursor.fetchall()
        else:
            raise ValueError("fetch_results is only supported for SQL databases")

    def close(self):
        if self.db_type in ["postgres", "mysql"]:
            self.cursor.close()
            self.conn.close()
        elif self.db_type == "mongo":
            self.client.close()
