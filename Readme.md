# Auth Plugin Library

![License](https://img.shields.io/badge/license-MIT-blue.svg)

A modular authentication library for Python applications, supporting JWT and OAuth2 authentication, with easy integration for multiple databases.

## Features

- **JWT Authentication**: Securely manage and validate JSON Web Tokens (JWT).
- **OAuth2 Authentication**: Easily integrate OAuth2 authentication for your application.
- **Database Flexibility**: Supports multiple databases, including MongoDB, MySQL, and PostgreSQL.
- **Modular Design**: Designed as plugins for seamless integration into existing projects.

## Installation

First, clone the repository:

```bash
git clone https://github.com/viseshagarwal/auth-plugin.git
cd auth-plugin
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

(Optional) If you want to install the package in editable mode:

```bash
pip install -e .
```

## Usage

### Basic Setup

To use the library, you need to create an instance of the authentication plugin and configure it according to your needs.

#### Example: JWT Authentication

```python
from auth_plugin.jwt_auth import JWTAuth
from auth_plugin.config import Config

config = Config(secret_key="your_secret_key")
jwt_auth = JWTAuth(config)

# Example usage
token = jwt_auth.create_token({"user_id": 1})
print(jwt_auth.verify_token(token))
```

#### Example: OAuth2 Authentication

```python
from auth_plugin.oauth2_auth import OAuth2Auth

oauth2_auth = OAuth2Auth(client_id="your_client_id", client_secret="your_client_secret")

# Example usage
auth_url = oauth2_auth.get_authorization_url()
print(auth_url)
```

### Database Integration

You can also connect to various databases using the `DBManager` class.

#### Example: MongoDB Integration

```python
from auth_plugin.db_manager import DBManager

db_manager = DBManager("mongodb", uri="mongodb://localhost:27017", db_name="auth_db")
collection = db_manager.get_collection("users")

# Example usage
user = collection.find_one({"username": "testuser"})
print(user)
```

## Running Tests

To run the unit tests for the library:

1. Ensure that the `auth_plugin` directory is on your `PYTHONPATH`:

   ```bash
   PYTHONPATH=. python -m unittest discover -s tests
   ```

2. Alternatively, you can run individual test files:

   ```bash
   python -m unittest tests/test_jwt_auth.py
   ```

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes. Make sure to include tests for any new functionality you add.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

## Key Sections Explained:

1. **Features**: Provides an overview of the capabilities of your library.
2. **Installation**: Explains how to set up the library, including installing dependencies and installing the package locally in editable mode.
3. **Usage**: Offers examples for the user on how to integrate the different features of your library into their projects.
4. **Database Integration**: Demonstrates how to connect to different databases.
5. **Running Tests**: Instructions for running the unit tests.
6. **Contributing**: Encourages others to contribute to the project.
7. **License**: Mentions the licensing terms.

This `README.md` should give users a good starting point to understand, install, and use your library. Feel free to modify the content according to your specific needs!
```
