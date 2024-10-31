from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from ..base import BaseDBManager
from ..exceptions import DBConnectionError, DBConfigurationError, DBOperationError


class PostgresDBManager(BaseDBManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = self.port or 5432
        self.connect()

    def connect(self) -> None:
        # try:
        #     connection_url = (
        #         f"postgresql://{self.user}:{self.password}@"
        #         f"{self.host}:{self.port}/{self.db_name}"
        #     )
        #     self.client = create_engine(
        #         connection_url,
        #         pool_pre_ping=True,
        #         pool_recycle=3600
        #     )
        #     self.db = self.client.connect()
        #     self.ping()
        #     self.logger.info("Successfully connected to PostgreSQL")
        try:
            connection_url = (
                f"postgresql://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.db_name}"
            )
            self.client = create_engine(
                connection_url,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.connection = self.client.connect()
            self.ping()
            self.logger.info("Successfully connected to PostgreSQL")

        except SQLAlchemyError as e:
            raise DBConnectionError(f"PostgreSQL connection failed: {str(e)}")

    def ping(self) -> bool:
        try:
            with self.db.begin():
                self.db.execute(text("SELECT 1"))
            return True
        except Exception as e:
            raise DBConnectionError(f"PostgreSQL ping failed: {str(e)}")

    def close(self) -> None:
        try:
            if self.db:
                self.db.close()
            if self.client:
                self.client.dispose()
            self.logger.info("PostgreSQL connection closed")
        except Exception as e:
            raise DBOperationError(
                f"Error closing PostgreSQL connection: {str(e)}")
