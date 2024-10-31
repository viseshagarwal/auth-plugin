from urllib.parse import quote_plus
from typing import Optional
from .exceptions import DBConfigurationError


class URIBuilder:
    @staticmethod
    def build_mongo_uri(host: str, port: int, user: Optional[str] = None, password: Optional[str] = None) -> str:
        try:
            credentials = f"{quote_plus(user)}:{quote_plus(
                password)}@" if user and password else ""
            return f"mongodb://{credentials}{host}:{port}"
        except Exception as e:
            raise DBConfigurationError(
                f"Failed to build MongoDB URI: {str(e)}")

    @staticmethod
    def build_sql_uri(db_type: str, host: str, port: int, db_name: str, user: str, password: str) -> str:
        try:
            credentials = f"{quote_plus(user)}:{quote_plus(password)}@"
            return f"{db_type}://{credentials}{host}:{port}/{db_name}"
        except Exception as e:
            raise DBConfigurationError(f"Failed to build SQL URI: {str(e)}")
