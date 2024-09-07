import pymongo
import psycopg2
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging


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

        try:
            if self.db_type == "mongo" or self.db_type == "mongodb":
                self.client = pymongo.MongoClient(host, port)
                self.db = self.client[db_name]
                logging.info("Connected to MongoDB database successfully")
            elif self.db_type == "postgres":
                self.conn = psycopg2.connect(
                    dbname=db_name, user=user, password=password, host=host, port=port
                )
                self.cursor = self.conn.cursor()
                logging.info("Connected to PostgreSQL database successfully")
            elif self.db_type == "mysql":
                self.conn = mysql.connector.connect(
                    host=host, user=user, password=password, database=db_name, port=port
                )
                self.cursor = self.conn.cursor(dictionary=True)
                logging.info("Connected to MySQL database successfully")
            else:
                raise ValueError("Unsupported database type")
        except (
            pymongo.errors.PyMongoError,
            psycopg2.Error,
            mysql.connector.Error,
        ) as e:
            logging.error(f"Database connection error: {str(e)}")
            raise RuntimeError(f"Failed to connect to {self.db_type} database")

    def get_collection(self, collection_name):
        if self.db_type == "mongo" or self.db_type == "mongodb":
            return self.db[collection_name]
        else:
            raise ValueError("get_collection is only supported for MongoDB")

    def execute_query(self, query, params=None):
        if self.db_type in ["postgres", "mysql"]:
            try:
                self.cursor.execute(query, params)
                self.conn.commit()
                logging.info("Query executed successfully")
            except (SQLAlchemyError, OperationalError) as e:
                logging.error(f"Error executing query: {str(e)}")
                raise RuntimeError("Query execution failed")
        else:
            raise ValueError("execute_query is only supported for SQL databases")

    def fetch_results(self):
        if self.db_type in ["postgres", "mysql"]:
            try:
                results = self.cursor.fetchall()
                logging.info("Results fetched successfully")
                return results
            except (SQLAlchemyError, OperationalError) as e:
                logging.error(f"Error fetching results: {str(e)}")
                raise RuntimeError("Failed to fetch results")
        else:
            raise ValueError("fetch_results is only supported for SQL databases")

    def close(self):
        try:
            if self.db_type in ["postgres", "mysql"]:
                self.cursor.close()
                self.conn.close()
                logging.info("SQL database connection closed successfully")
            elif self.db_type == "mongo" or self.db_type == "mongodb":
                self.client.close()
                logging.info("MongoDB connection closed successfully")
        except (SQLAlchemyError, OperationalError, pymongo.errors.PyMongoError) as e:
            logging.error(f"Error closing database connection: {str(e)}")
            raise RuntimeError("Failed to close the database connection")
