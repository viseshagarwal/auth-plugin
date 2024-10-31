"""JWT Authentication Plugin

A robust Python library for JWT token generation, validation and management.
Supports both HS256 and RS256 algorithms with token blacklisting capabilities.
"""

from .plugin import JWTAuthPlugin
from .config import TokenConfig
from .exceptions import (
    JWTError,
    JWTTokenExpiredError,
    JWTInvalidTokenError,
    JWTBlacklistedError,
    JWTConfigurationError,
    JWTSignatureError,
    JWTAlgorithmError
)

__version__ = "0.5.0"
__author__ = "Visesh Agarwal"

__all__ = [
    # Main classes
    'JWTAuthPlugin',
    'TokenConfig',

    # Exceptions
    'JWTError',
    'JWTTokenExpiredError',
    'JWTInvalidTokenError',
    'JWTBlacklistedError',
    'JWTConfigurationError',
    'JWTSignatureError',
    'JWTAlgorithmError'
]
