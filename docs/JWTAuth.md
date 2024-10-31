# JWTAuth Plugin Documentation

## Overview

JWTAuth is a robust Python library for JWT (JSON Web Token) authentication with support for both HS256 and RS256 algorithms, token blacklisting, and refresh token functionality.

## Installation

```bash
pip install auth-plugin
```

## Basic Usage

```python

from auth_plugin import JWTAuthPlugin, TokenConfig

# Create configuration
config = TokenConfig(
    secret_key="your-secret-key",
    algorithm="HS256",
    access_token_expiry=3600,  # 1 hour
    refresh_token_expiry=86400  # 24 hours
)

# Initialize plugin
auth = JWTAuthPlugin(config)

# Generate tokens
user_data = {"user_id": "123", "username": "john_doe"}
access_token, refresh_token = auth.generate_tokens(user_data)

# Verify token
payload = auth.verify_token(access_token)

# Refresh token
new_access_token = auth.refresh_access_token(refresh_token)

```

### Configuration Options

#### **TokenConfig Parameters**

- **`secret_key`** (str, required):
  - Secret key for HS256 or key identifier for RS256.
- **`algorithm`** (str, optional):
  - Supported algorithms are "HS256" (default) or "RS256".
- **`access_token_expiry`** (int, optional):
  - Sets the expiry time in seconds for access tokens (default: 3600 seconds).
- **`refresh_token_expiry`** (int, optional):
  - Sets the expiry time in seconds for refresh tokens (default: 86400 seconds).
- **`private_key`** (bytes, optional):
  - RSA private key for RS256 encryption.
- **`public_key`** (bytes, optional):
  - RSA public key for RS256 encryption.
- **`issuer`** (str, optional):
  - Defines the token issuer claim.
- **`audience`** (str, optional):
  - Defines the token audience claim.

---

### API Reference

#### **JWTAuthPlugin Methods**

1. **`generate_tokens(payload: Dict) -> Tuple[str, str]`**

   - **Description**: Generates access and refresh tokens.
   - **Parameters**:
     - `payload`: Dictionary containing claims to encode in token.
   - **Returns**: Tuple with `(access_token, refresh_token)`.

2. **`verify_token(token: str, token_type: str = "access") -> Dict`**

   - **Description**: Verifies and decodes a token.
   - **Parameters**:
     - `token`: JWT token string.
     - `token_type`: "access" or "refresh" (default: "access").
   - **Returns**: Dictionary containing decoded token claims.

3. **`refresh_access_token(refresh_token: str) -> str`**

   - **Description**: Generates a new access token using a refresh token.
   - **Parameters**:
     - `refresh_token`: Valid refresh token.
   - **Returns**: New access token.

4. **`blacklist_token(token: str) -> None`**

   - **Description**: Adds a token to the blacklist.
   - **Parameters**:
     - `token`: Token to blacklist.

5. **`clean_blacklist() -> None`**
   - **Description**: Removes expired tokens from the blacklist.

---

### Static Methods

1. **`generate_rsa_keys(key_size: int = 2048) -> Tuple[bytes, bytes]`**
   - **Description**: Generates an RSA key pair.
   - **Parameters**:
     - `key_size`: Size of RSA key in bits (default: 2048).
   - **Returns**: Tuple with `(private_key, public_key)` in PEM format.

---

### Usage Examples

- **Using RS256 Algorithm**

```python
from auth_plugin import JWTAuthPlugin, TokenConfig

# Generate RSA keys
private_key, public_key = JWTAuthPlugin.generate_rsa_keys()

config = TokenConfig(
    secret_key="key-id",
    algorithm="RS256",
    private_key=private_key,
    public_key=public_key
)

auth = JWTAuthPlugin(config)
```

- **Token Blacklisting**

```python
# Blacklist a token
  auth.blacklist_token(access_token)


# Clean expired tokens from blacklist

auth.clean_blacklist()

```

- **Error Handling**

```python
from auth_plugin import JWTError

try:
    payload = auth.verify_token(token)
except JWTError as e:
    print(f"Token validation failed: {e}")

```

---

### Security Considerations

1. **Secret Key Protection**

   - Use strong secret keys.
   - Store keys securely.
   - Rotate keys periodically.

2. **Token Expiration**

   - Use short expiration times for access tokens.
   - Use longer expiration for refresh tokens.
   - Implement a token refresh flow.

3. **Token Validation**

   - Always verify the token signature.
   - Validate token expiration.
   - Check token type before use.

4. **RS256 vs. HS256**
   - Use RS256 for distributed systems.
   - Use HS256 for single-server applications.
   - Ensure private keys are protected when using RS256.
