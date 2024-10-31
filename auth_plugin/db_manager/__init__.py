import logging
from .handlers.mongo import MongoDBManager
from .handlers.postgres import PostgresDBManager
from .handlers.mysql import MySQLManager
from .exceptions import DBConfigurationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_db_manager(db_type: str, **kwargs):
    """
    Factory function to create appropriate database manager instance.

    Args:
        db_type: Type of database ('mongodb', 'postgresql', 'mysql')
        **kwargs: Configuration parameters for database connection

    Returns:
        Database manager instance
    """
    db_types = {
        'mongodb': MongoDBManager,
        'mongo': MongoDBManager,
        'postgresql': PostgresDBManager,
        'mysql': MySQLManager
    }

    manager_class = db_types.get(db_type.lower())
    if not manager_class:
        raise DBConfigurationError(f"Unsupported database type: {db_type}")

    return manager_class(**kwargs)


__all__ = ['create_db_manager']
