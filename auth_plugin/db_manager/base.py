from abc import ABC, abstractmethod
from typing import Optional, Any
import logging


class BaseDBManager(ABC):
    """Abstract base class for database managers"""

    def __init__(
        self,
        db_name: str,
        host: str = "localhost",
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        connection_timeout: int = 5000,
        **kwargs: Any
    ):
        self.db_name = db_name
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection_timeout = connection_timeout
        self.client = None
        self.db = None
        self.connection = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close database connection"""
        pass

    @abstractmethod
    def ping(self) -> bool:
        """Test database connection"""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def conn(self):
        """Direct access to database connection"""
        return self.connection
