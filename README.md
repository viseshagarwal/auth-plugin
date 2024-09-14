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

The `DBManager` class supports connections to MongoDB, PostgreSQL and MySQL. Use the appropriate database type when initializing the object.

#### MongoDB

```python
from auth_plugin.db_manager import DBManager

db_manager = DBManager(
    db_type="mongodb",  # or "mongo"
    host="localhost",
    port=27017,
    db_name="testdb"
)
```

#### PostgreSQL

```python
db_manager = DBManager(
    db_type="postgres",
    user="username",
    password="password",
    host="localhost",
    port=5432,
    db_name="testdb"
)
```

#### MySQL

```python
db_manager = DBManager(
    db_type="mysql",
    user="username",
    password="password",
    host="localhost",
    db_name="testdb"
)
```

### Query Execution for All Supported Databases

The `DBManager` class provides methods for executing queries and fetching results. The behavior is different depending on whether you're using an SQL database (PostgreSQL, MySQL, SQLite) or a NoSQL database like MongoDB.

#### SQL Databases (PostgreSQL, MySQL)

For SQL-based databases (PostgreSQL and MySQL), you can execute SQL queries and fetch results using the following methods:

```python
# Execute a query (e.g., creating a table)
db_manager.execute_query("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255))")

# Insert data into the table
db_manager.execute_query("INSERT INTO users (name) VALUES (%s)", ("John Doe",))

# Fetch all results from a table
db_manager.execute_query("SELECT * FROM users")
results = db_manager.fetch_results()
print(results)
```

#### MongoDB

For MongoDB, you can interact with collections using the `get_collection` method, and perform operations like inserting or querying documents.

```python
# Get a collection
collection = db_manager.get_collection("users")

# Insert a document into the collection
collection.insert_one({"name": "John Doe"})

# Query documents from the collection
results = collection.find({"name": "John Doe"})
for doc in results:
    print(doc)
```

### Closing the Connection

After executing queries or performing operations, don't forget to close the connection.

```python
db_manager.close()
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

This project is licensed under the MIT License - see the [LICENSE](https://github.com/viseshagarwal/auth-plugin/blob/main/LICENSE) file for details.
