# Auth Plugin Library

**Auth Plugin** is a robust and flexible Python library designed to streamline the authentication process in web applications. It provides built-in support for JWT authentication, OAuth2 token management, and seamless database connectivity with MongoDB, PostgreSQL, and MySQL.

### Features

- **JWT Authentication**: Easily encode and decode JSON Web Tokens (JWTs) with built-in error handling.
- **OAuth2 Integration**: Fetch and manage OAuth2 tokens with automatic error handling for HTTP requests.
- **Database Connectivity**: Connect to MongoDB, PostgreSQL, and MySQL databases with a simple API and proper connection management.
- **Robust Error Handling**: Comprehensive `try-except` blocks across all operations, ensuring stability and reliability.
- **Logging**: Configurable logging for all operations, including JWT processing, OAuth2 token management, and database connections.

### Installation

```bash
pip install auth-plugin
```

### Usage

#### JWT Authentication

```python
from auth_plugin.jwt_auth import JWTAuth

jwt_auth = JWTAuth(secret_key="your_secret_key")
token = jwt_auth.encode_token({"user_id": 123})
payload = jwt_auth.decode_token(token)
```

#### Database Management

```python
from auth_plugin.db_manager import DBManager

# MongoDB
db_manager = DBManager(db_type="mongodb", host="localhost", port=27017, db_name="testdb")

# PostgreSQL
db_manager = DBManager(db_type="postgresql", user="username", password="password", host="localhost", port=5432, db_name="testdb")

# MySQL
db_manager = DBManager(db_type="mysql", user="username", password="password", host="localhost", db_name="testdb")
```

#### OAuth2 Authentication

```python
from auth_plugin.oauth2_auth import OAuth2Auth

oauth2 = OAuth2Auth(client_id="your_client_id", client_secret="your_client_secret", token_url="https://example.com/oauth2/token")
access_token = oauth2.get_access_token(grant_type="client_credentials")
```

### Documentation

Please refer to the [official documentation](https://github.com/viseshagarwal/auth-plugin) for detailed usage instructions and examples.

### Contributing

Contributions are welcome! Please check the [contributing guidelines](https://github.com/viseshagarwal/auth-plugin) before submitting a pull request.
