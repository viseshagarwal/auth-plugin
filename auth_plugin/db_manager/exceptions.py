class DBError(Exception):
    """Base class for database exceptions"""
    pass


class DBConnectionError(DBError):
    """Raised when database connection fails"""
    pass


class DBAuthenticationError(DBError):
    """Raised when authentication fails"""
    pass


class DBConfigurationError(DBError):
    """Raised when database configuration is invalid"""
    pass


class DBOperationError(DBError):
    """Raised when database operation fails"""
    pass
