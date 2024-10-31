# import pymongo
# import psycopg2
# from sqlalchemy import create_engine
# from sqlalchemy.exc import SQLAlchemyError, OperationalError
# import logging
# from typing import Optional
# from urllib.parse import quote_plus


# class DBManager:
#     def __init__(
#         self,
#         db_type: str,
#         db_name: str,
#         host: str = "localhost",
#         port: Optional[int] = None,
#         user: Optional[str] = None,
#         password: Optional[str] = None,
#         connection_timeout: int = 5000
#     ):
#         """Initialize database connection manager.

#         Args:
#             db_type: Type of database ('mongo'/'mongodb' or 'postgresql')
#             db_name: Name of the database
#             host: Database host address
#             port: Database port number
#             user: Database username
#             password: Database password
#             connection_timeout: Connection timeout in milliseconds
#         """
#         self.db_type = db_type.lower()
#         self.db_name = db_name
#         self.host = host
#         self.port = port or self._get_default_port()
#         self.user = user
#         self.password = password
#         self.connection_timeout = connection_timeout
#         self.client = None
#         self.db = None

#         self._connect()

#     def _get_default_port(self) -> int:
#         """Get default port for database type."""
#         defaults = {
#             "mongodb": 27017,
#             "mongo": 27017,
#             "postgresql": 5432
#         }
#         return defaults.get(self.db_type, 27017)

#     def _connect(self) -> None:
#         """Establish database connection."""
#         try:
#             if self.db_type in ["mongo", "mongodb"]:
#                 uri = self._build_mongo_uri()
#                 self.client = pymongo.MongoClient(
#                     uri,
#                     serverSelectionTimeoutMS=self.connection_timeout
#                 )
#                 # Test connection
#                 self.client.server_info()
#                 self.db = self.client[self.db_name]
#                 logging.info("Successfully connected to MongoDB database")
#             else:
#                 raise ValueError(f"Unsupported database type: {self.db_type}")

#         except pymongo.errors.ServerSelectionTimeoutError:
#             logging.error("Failed to connect to MongoDB: Connection timed out")
#             raise
#         except pymongo.errors.ConnectionError as e:
#             logging.error(f"Failed to connect to MongoDB: {str(e)}")
#             raise
#         except Exception as e:
#             logging.error(
#                 f"Unexpected error while connecting to database: {str(e)}")
#             raise

#     def _build_mongo_uri(self) -> str:
#         """Build MongoDB connection URI."""
#         if self.user and self.password:
#             credentials = f"{quote_plus(self.user)}:{
#                 quote_plus(self.password)}@"
#         else:
#             credentials = ""

#         return f"mongodb://{credentials}{self.host}:{self.port}"

#     def close(self) -> None:
#         """Close database connection."""
#         try:
#             if self.client:
#                 self.client.close()
#                 logging.info("Database connection closed successfully")
#         except Exception as e:
#             logging.error(f"Error closing database connection: {str(e)}")
#             raise

#     def __enter__(self):
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.close()
