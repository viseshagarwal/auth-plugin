# Auth Plugin Library

**Auth Plugin** is a robust and flexible Python library designed to streamline the authentication process in web applications. It provides built-in support for JWT authentication, OAuth2 token management, and seamless database connectivity with MongoDB, PostgreSQL, and MySQL.

## Features

- **JWT Authentication**: Easily encode and decode JSON Web Tokens (JWTs) with built-in error handling and robust security.
- **OAuth2 Integration**: Fetch and manage OAuth2 tokens with automatic error handling for HTTP requests and support for various grant types.
- **Database Connectivity**: Connect to MongoDB, PostgreSQL, and MySQL databases with a simple API and proper connection management.
- **Robust Error Handling**: Comprehensive `try-except` blocks across all operations, ensuring stability and reliability.
- **Configurable Logging**: Detailed logging for all operations, including JWT processing, OAuth2 token management, and database connections.

## Installation

To install the Auth Plugin library, use pip:

```bash
pip install auth-plugin
```

## Usage

### JWT Authentication

The JWT authentication module allows you to encode and decode JSON Web Tokens.

```python
from auth_plugin.jwt_auth import JWTAuth

# Initialize the JWTAuth object with a secret key
jwt_auth = JWTAuth(secret_key="your_secret_key")

# Encode a payload to generate a JWT token
token = jwt_auth.encode_token({"user_id": 123})

# Decode the JWT token to retrieve the payload
payload = jwt_auth.decode_token(token)
```

### Database Management

The DBManager class supports connections to MongoDB, PostgreSQL, and MySQL. Use the appropriate database type when initializing the object.

```python
from auth_plugin.db_manager import DBManager

# MongoDB
db_manager = DBManager(
    db_type="mongodb", # or "mongo"
    host="localhost",
    port=27017,
    db_name="testdb"
)

# PostgreSQL
db_manager = DBManager(
    db_type="postgresql",
    user="username",
    password="password",
    host="localhost",
    port=5432,
    db_name="testdb"
)

# MySQL
db_manager = DBManager(
    db_type="mysql",
    user="username",
    password="password",
    host="localhost",
    db_name="testdb"
)
```

### OAuth2 Authentication

The OAuth2 authentication module allows you to obtain access tokens using the OAuth2 protocol.

```python
from auth_plugin.oauth2_auth import OAuth2Auth

# Initialize the OAuth2Auth object with client credentials and token URL
oauth2 = OAuth2Auth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="http://localhost/callback",
    auth_url="https://example.com/oauth2/authorize",
    token_url="https://example.com/oauth2/token"
)

# Generate the authorization URL
authorization_url = oauth2.get_authorization_url()

# Exchange the authorization code for an access token
access_token = oauth2.get_access_token(code="authorization_code")
```

## Documentation

For detailed usage instructions, examples, and API reference, please refer to the [official documentation](https://github.com/viseshagarwal/auth-plugin).

## Contributing

Contributions are welcome! If you'd like to contribute to the Auth Plugin library, please follow our [contributing guidelines](https://github.com/viseshagarwal/auth-plugin). Ensure you have reviewed the guidelines before submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/viseshagarwal/auth-plugin/LICENSE.md) file for details.
