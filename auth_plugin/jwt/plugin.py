import jwt
import datetime
import logging
from typing import Dict, Any, Tuple, Set
from .config import TokenConfig
from .exceptions import JWTError
from .utils import generate_rsa_keys

logger = logging.getLogger(__name__)


class JWTAuthPlugin:
    """JWT Authentication Plugin"""
    MAX_BLACKLIST_SIZE: int = 1000

    def __init__(self, config: TokenConfig):
        self.config = config
        self._blacklisted_tokens: Set[str] = set()

        if config.algorithm.startswith("RS") and (not config.private_key or not config.public_key):
            private_key, public_key = self.generate_rsa_keys()
            self.config.private_key = private_key
            self.config.public_key = public_key

    @staticmethod
    def generate_rsa_keys() -> Tuple[bytes, bytes]:
        """Generate RSA private and public keys

        Returns: `tuple` [bytes, bytes]: Private and public keys

        Example:
            >>> private_key, public_key = JWTAuthPlugin.generate_rsa_keys()    
            """
        return generate_rsa_keys()

    def generate_tokens(self, user_data: Dict[str, Any]) -> Tuple[str, str]:
        """Generate access and refresh tokens

    Args:
        user_data (Dict[str, Any]): User data to encode in token

    Returns:
        Tuple[str, str]: Access token and refresh token

    Raises:
        JWTError: If token generation fails

    Example:
        >>> auth = JWTAuthPlugin(config)
        >>> access_token, refresh_token = auth.generate_tokens({"user_id": 123})
    """
        try:
            access_token = self._create_token(
                payload={**user_data, "type": "access"},
                expiry=self.config.access_token_expiry
            )

            refresh_token = self._create_token(
                payload={**user_data, "type": "refresh"},
                expiry=self.config.refresh_token_expiry
            )

            return access_token, refresh_token
        except Exception as e:
            raise JWTError(f"Token generation failed: {str(e)}")

    def _create_token(self, payload: Dict[str, Any], expiry: int) -> str:
        """Create a JWT token with specified payload and expiry"""
        try:
            token_payload = {
                **payload,
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expiry),
                "iat": datetime.datetime.now(datetime.timezone.utc)
            }

            if self.config.algorithm.startswith("RS"):
                return jwt.encode(token_payload, self.config.private_key, algorithm=self.config.algorithm)
            return jwt.encode(token_payload, self.config.secret_key, algorithm=self.config.algorithm)
        except Exception as e:
            raise JWTError(f"Token creation failed: {str(e)}")

    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verify and decode a JWT token

        Args:
            token (str): Token to verify
            token_type (str): Expected token type ("access" or "refresh")

        Returns:
            Dict[str, Any]: Decoded token payload

        Raises:
            JWTError: If token verification fails
        """
        if token in self._blacklisted_tokens:
            raise JWTError("Token has been blacklisted")

        if not token:
            # Changed from JWTInvalidTokenError
            raise JWTError("Invalid token format")

        # Validate token structure
        if not isinstance(token, str) or token.count('.') != 2:
            raise JWTError("Invalid token format")

        try:
            key = self.config.public_key if self.config.algorithm.startswith(
                "RS") else self.config.secret_key

            # Decode token with strict validation
            payload = jwt.decode(
                token,
                key,
                algorithms=[self.config.algorithm],
                options={
                    'verify_signature': True,
                    'verify_exp': True,
                    'verify_iat': True,
                    'require': ['exp', 'iat', 'type']
                }
            )

            # Validate token type
            if payload.get("type") != token_type:
                raise JWTError("Invalid token type")

            return payload

        except jwt.ExpiredSignatureError:
            raise JWTError("Token has expired")
        except jwt.InvalidSignatureError:
            raise JWTError("Invalid token signature")
        except jwt.InvalidTokenError:
            raise JWTError("Invalid token format")
        except Exception as e:
            raise JWTError(f"Token verification failed: {str(e)}")

    def refresh_access_token(self, refresh_token: str) -> str:
        """ Refresh access token using refresh token

        Args:
            refresh_token (str): Refresh token to use

        Returns:
            str: New access token

        Raises:
            WTError: If token refresh fails

        Example:
            >>> auth = JWTAuthPlugin(config)
            >>> new_access_token = auth.refresh_access_token(refresh_token)
"""
        try:
            payload = self.verify_token(refresh_token, token_type="refresh")
            payload.pop("exp", None)
            payload.pop("iat", None)
            payload["type"] = "access"

            return self._create_token(payload, self.config.access_token_expiry)
        except Exception as e:
            raise JWTError(f"Token refresh failed: {str(e)}")

    def blacklist_token(self, token: str) -> None:
        """Add token to blacklist

        Args:
            token (str): Token to blacklist

        Example:
            >>> auth = JWTAuthPlugin(config)
            >>> auth.blacklist_token(access_token)

        """

        self._blacklisted_tokens.add(token)

    def clean_blacklist(self) -> None:
        """Remove expired tokens from blacklist

        Example:
            >>> auth = JWTAuthPlugin(config)
            >>> auth.clean_blacklist()
        """
        current_time = datetime.datetime.now(datetime.timezone.utc)
        self._blacklisted_tokens = {
            token for token in self._blacklisted_tokens
            if not self._is_token_expired(token)
        }

    def _is_token_expired(self, token: str) -> bool:
        """Check if token has expired

        Args:
            token (str): Token to check

        Returns:
            bool: True if token has expired

        """
        try:
            # Decode without verification to extract exp claim
            payload = jwt.decode(
                token,
                options={
                    'verify_signature': False,
                    'verify_exp': False
                }
            )

            # Check if token has expired
            exp_timestamp = payload.get('exp')
            if not exp_timestamp:
                return True

            exp_time = datetime.datetime.fromtimestamp(
                exp_timestamp, tz=datetime.timezone.utc)
            current_time = datetime.datetime.now(datetime.timezone.utc)

            return current_time > exp_time

        except Exception:
            return True
