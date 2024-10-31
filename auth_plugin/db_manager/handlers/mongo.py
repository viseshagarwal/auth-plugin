import pymongo
from ..base import BaseDBManager
from ..exceptions import DBConnectionError, DBAuthenticationError, DBOperationError


class MongoDBManager(BaseDBManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = self.port or 27017
        self.connect()

    def connect(self) -> None:
        try:
            connection_url = f"mongodb://"
            if self.user and self.password:
                connection_url += f"{self.user}:{self.password}@"
            connection_url += f"{self.host}:{self.port}"

            self.client = pymongo.MongoClient(
                connection_url,
                serverSelectionTimeoutMS=self.connection_timeout
            )
            self.db = self.client[self.db_name]
            self.ping()  # Test connection
            self.logger.info("Successfully connected to MongoDB")

        except pymongo.errors.ServerSelectionTimeoutError:
            raise DBConnectionError("MongoDB connection timed out")
        except pymongo.errors.OperationFailure as e:
            if "Authentication failed" in str(e):
                raise DBAuthenticationError("Invalid MongoDB credentials")
            raise DBOperationError(f"MongoDB operation failed: {str(e)}")

    def ping(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            raise DBConnectionError(f"MongoDB ping failed: {str(e)}")

    def close(self) -> None:
        try:
            if self.client:
                self.client.close()
                self.logger.info("MongoDB connection closed")
        except Exception as e:
            raise DBOperationError(
                f"Error closing MongoDB connection: {str(e)}")
