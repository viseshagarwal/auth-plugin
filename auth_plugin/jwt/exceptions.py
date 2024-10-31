from typing import Optional


class JWTError(Exception):
    def __init__(self, message: str, error_code: str = "JWT_ERROR") -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class JWTTokenExpiredError(JWTError):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, "TOKEN_EXPIRED")


class JWTInvalidTokenError(JWTError):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message, "INVALID_TOKEN")


class JWTBlacklistedError(JWTError):
    def __init__(self, message: str = "Token has been blacklisted"):
        super().__init__(message, "TOKEN_BLACKLISTED")


class JWTConfigurationError(JWTError):
    def __init__(self, message: str = "Invalid configuration"):
        super().__init__(message, "CONFIG_ERROR")


class JWTSignatureError(JWTError):
    def __init__(self, message: str = "Invalid token signature"):
        super().__init__(message, "INVALID_SIGNATURE")


class JWTAlgorithmError(JWTError):
    def __init__(self, message: str = "Unsupported algorithm"):
        super().__init__(message, "ALGORITHM_ERROR")
