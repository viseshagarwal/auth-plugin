import pytest
import jwt
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from auth_plugin.jwt import JWTAuthPlugin, TokenConfig, JWTError


class TestJWTAuthPlugin:
    @pytest.fixture
    def hs256_config(self):
        return TokenConfig(
            secret_key="test-secret-key",
            algorithm="HS256",
            access_token_expiry=300,
            refresh_token_expiry=3600
        )

    @pytest.fixture
    def rs256_config(self):
        private_key, public_key = JWTAuthPlugin.generate_rsa_keys()
        return TokenConfig(
            secret_key="test-key",
            algorithm="RS256",
            private_key=private_key,
            public_key=public_key,
            access_token_expiry=300,
            refresh_token_expiry=3600
        )

    @pytest.fixture
    def user_data(self):
        return {
            "user_id": "123",
            "username": "test_user",
            "role": "admin"
        }

    def test_hs256_token_generation(self, hs256_config, user_data):
        jwt_auth = JWTAuthPlugin(hs256_config)
        access_token, refresh_token = jwt_auth.generate_tokens(user_data)

        # Verify access token
        payload = jwt_auth.verify_token(access_token, "access")
        assert payload["user_id"] == user_data["user_id"]
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload

        # Verify refresh token
        payload = jwt_auth.verify_token(refresh_token, "refresh")
        assert payload["user_id"] == user_data["user_id"]
        assert payload["type"] == "refresh"

    def test_rs256_token_generation(self, rs256_config, user_data):
        jwt_auth = JWTAuthPlugin(rs256_config)
        access_token, refresh_token = jwt_auth.generate_tokens(user_data)

        payload = jwt_auth.verify_token(access_token)
        assert payload["user_id"] == user_data["user_id"]

    def test_token_expiration(self, hs256_config, user_data):
        config = TokenConfig(
            secret_key="test-key",
            algorithm="HS256",
            access_token_expiry=1  # 1 second
        )
        jwt_auth = JWTAuthPlugin(config)
        access_token, _ = jwt_auth.generate_tokens(user_data)

        time.sleep(2)
        with pytest.raises(JWTError) as exc:
            jwt_auth.verify_token(access_token)
        assert "expired" in str(exc.value)

    def test_token_refresh(self, hs256_config, user_data):
        jwt_auth = JWTAuthPlugin(hs256_config)
        _, refresh_token = jwt_auth.generate_tokens(user_data)

        new_access_token = jwt_auth.refresh_access_token(refresh_token)
        payload = jwt_auth.verify_token(new_access_token, "access")
        assert payload["user_id"] == user_data["user_id"]

    def test_clean_blacklist(self, hs256_config, user_data):
        config = TokenConfig(
            secret_key="test-secret-key",
            algorithm="HS256",
            access_token_expiry=1,  # 1 second expiry
            refresh_token_expiry=2
        )
        jwt_auth = JWTAuthPlugin(config)
        access_token, _ = jwt_auth.generate_tokens(user_data)

        jwt_auth.blacklist_token(access_token)
        assert access_token in jwt_auth._blacklisted_tokens

        time.sleep(2)  # Wait for token to expire
        jwt_auth.clean_blacklist()
        assert access_token not in jwt_auth._blacklisted_tokens

    def test_invalid_token_signature(self, hs256_config, user_data):
        jwt_auth = JWTAuthPlugin(hs256_config)
        token = jwt.encode(
            {"user_id": "123"},
            "wrong_secret",
            algorithm="HS256"
        )
        with pytest.raises(JWTError) as exc:
            jwt_auth.verify_token(token)
        assert "signature" in str(exc.value)

    def test_token_type_validation(self, hs256_config, user_data):
        jwt_auth = JWTAuthPlugin(hs256_config)
        access_token, refresh_token = jwt_auth.generate_tokens(user_data)

        with pytest.raises(JWTError, match="Invalid token type"):
            jwt_auth.verify_token(access_token, "refresh")
        with pytest.raises(JWTError, match="Invalid token type"):
            jwt_auth.verify_token(refresh_token, "access")

    def test_invalid_token_format(self, hs256_config):
        jwt_auth = JWTAuthPlugin(hs256_config)
        invalid_tokens = ["invalid", "a.b", "a.b.c.d", None]

        for token in invalid_tokens:
            with pytest.raises(JWTError) as exc:
                jwt_auth.verify_token(token)
            assert "invalid token" in str(exc.value).lower()

    def test_config_validation(self):
        with pytest.raises(JWTError, match="secret_key is required"):
            TokenConfig(secret_key="")

        with pytest.raises(JWTError):
            TokenConfig(
                secret_key="test",
                algorithm="INVALID"
            )

        with pytest.raises(JWTError):
            TokenConfig(
                secret_key="test",
                access_token_expiry=-1
            )
