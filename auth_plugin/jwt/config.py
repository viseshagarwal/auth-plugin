from dataclasses import dataclass
from typing import Optional
from .exceptions import JWTConfigurationError


@dataclass
class TokenConfig:
    """
    Configuration class for JWT token generation and validation.

    Attributes:
    secret_key (str): The secret key used to sign the JWT token.
    algorithm (str): The algorithm used to sign the JWT token. Default is HS256.
    access_token_expiry (int): The expiry time for the access token in seconds. Default is 3600 seconds.
    refresh_token_expiry (int): The expiry time for the refresh token in seconds. Default is 86400
    issuer (str): The issuer of the JWT token. Default is None.
    audience (str): The audience of the JWT token. Default is None.
    private_key (bytes): The private key used for RS256 algorithm. Default is None.
    public_key (bytes): The public key used for RS256 algorithm. Default is None.
    min_key_size (int): The minimum key size for the RSA algorithm. Default is 2048 bits.
    max_blacklist_size (int): The maximum size of the token blacklist. Default is 1000.

    Raises:
    JWTConfigurationError: If the secret_key is not provided or if the algorithm is not supported.
    JWTConfigurationError: If the access_token_expiry is not positive or if the refresh_token_expiry is less than access_token_expiry.

    """
    secret_key: str
    algorithm: str = "HS256"
    access_token_expiry: int = 3600
    refresh_token_expiry: int = 86400
    issuer: Optional[str] = None
    audience: Optional[str] = None
    private_key: Optional[bytes] = None
    public_key: Optional[bytes] = None
    min_key_size: int = 2048
    max_blacklist_size: int = 1000

    def __post_init__(self):
        if not self.secret_key:
            raise JWTConfigurationError("secret_key is required")

        allowed_algorithms = ["HS256", "HS384",
                              "HS512", "RS256", "RS384", "RS512"]
        if self.algorithm not in allowed_algorithms:
            raise JWTConfigurationError(
                f"Algorithm must be one of {allowed_algorithms}")

        if self.access_token_expiry <= 0:
            raise JWTConfigurationError("access_token_expiry must be positive")

        if self.refresh_token_expiry <= self.access_token_expiry:
            raise JWTConfigurationError(
                "refresh_token_expiry must be greater than access_token_expiry")
