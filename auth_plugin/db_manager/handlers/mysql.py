# from sqlalchemy import create_engine
# from sqlalchemy.exc import SQLAlchemyError
# import mysql.connector
# from ..base import BaseDBManager
# from ..exceptions import DBConnectionError, DBConfigurationError, DBOperationError


# class MySQLManager(BaseDBManager):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.port = self.port or 3306
#         if not (self.user and self.password):
#             raise DBConfigurationError("MySQL requires authentication")
#         self.connect()

#     def connect(self) -> None:
#         try:
#             connection_url = (
#                 f"mysql+mysqlconnector://{self.user}:{self.password}@"
#                 f"{self.host}:{self.port}/{self.db_name}"
#             )
#             self.client = create_engine(connection_url)
#             self.db = self.client.connect()
#             self.ping()
#             self.logger.info("Successfully connected to MySQL")

#         except SQLAlchemyError as e:
#             raise DBConnectionError(f"MySQL connection failed: {str(e)}")
#         except mysql.connector.Error as e:
#             raise DBConnectionError(f"MySQL error: {str(e)}")

#     def ping(self) -> bool:
#         try:
#             self.db.execute("SELECT 1")
#             return True
#         except Exception as e:
#             raise DBConnectionError(f"MySQL ping failed: {str(e)}")

#     def close(self) -> None:
#         try:
#             if self.db:
#                 self.db.close()
#             if self.client:
#                 self.client.dispose()
#             self.logger.info("MySQL connection closed")
#         except Exception as e:
#             raise DBOperationError(f"Error closing MySQL connection: {str(e)}")
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import mysql.connector
from ..base import BaseDBManager
from ..exceptions import DBConnectionError, DBConfigurationError, DBOperationError


class MySQLManager(BaseDBManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = self.port or 3306
        if not (self.user and self.password):
            raise DBConfigurationError("MySQL requires authentication")
        self.connect()

    def connect(self) -> None:
        try:
            # Use mysqlconnector driver for better compatibility
            connection_url = (
                f"mysql+mysqlconnector://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.db_name}"
            )
            self.client = create_engine(
                connection_url,
                pool_pre_ping=True,  # Enable connection health checks
                pool_recycle=3600    # Recycle connections after 1 hour
            )
            self.db = self.client.connect()
            self.ping()  # Verify connection
            self.logger.info("Successfully connected to MySQL")

        except SQLAlchemyError as e:
            raise DBConnectionError(f"MySQL connection failed: {str(e)}")
        except mysql.connector.Error as e:
            raise DBConnectionError(f"MySQL error: {str(e)}")

    def ping(self) -> bool:
        try:
            # Use text() to create executable SQL statement
            with self.db.begin():
                self.db.execute(text("SELECT 1"))
            return True
        except Exception as e:
            raise DBConnectionError(f"MySQL ping failed: {str(e)}")

    def close(self) -> None:
        try:
            if self.db:
                self.db.close()
            if self.client:
                self.client.dispose()
            self.logger.info("MySQL connection closed")
        except Exception as e:
            raise DBOperationError(f"Error closing MySQL connection: {str(e)}")
