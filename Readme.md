# Auth Plugin Library

## Overview

`auth-plugin` is a Python library designed to streamline the authentication process across different applications. It provides a flexible and extensible framework that supports multiple authentication methods, including JWT and OAuth2, with the ability to connect to various databases.

## Features

- **Pluggable Authentication**: Easily switch between different authentication methods like JWT and OAuth2.
- **Database Integration**: Connect seamlessly to different databases such as MongoDB, PostgreSQL, and more.
- **Utility Functions**: Includes helper functions to support common authentication and security tasks.
- **Extensible**: Easily add new authentication methods or databases.

## Installation

To install the library, clone the repository and install the dependencies:

```bash
git clone https://github.com/viseshagarwal/auth-plugin.git
cd auth-plugin
pip install -e .
```

Make sure you have all required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. **JWT Authentication**

To use JWT authentication, first import the `JWTAuth` class:

```python
from auth_plugin.jwt_auth import JWTAuth

jwt_auth = JWTAuth(secret_key="your_secret_key")
token = jwt_auth.create_token({"user_id": 123})
is_valid = jwt_auth.verify_token(token)
```

### 2. **OAuth2 Authentication**

To use OAuth2 authentication, import the `OAuth2Auth` class:

```python
from auth_plugin.oauth2_auth import OAuth2Auth

oauth2_auth = OAuth2Auth(client_id="your_client_id", client_secret="your_client_secret")
authorization_url = oauth2_auth.get_authorization_url(redirect_uri="https://yourapp.com/callback")
token = oauth2_auth.exchange_code_for_token(code="authorization_code", redirect_uri="https://yourapp.com/callback")
```

### 3. **Database Integration**

#### Connecting to MongoDB

```python
from auth_plugin.db_manager import DBManager

db_manager = DBManager(db_type="mongo", db_name="your_db_name", host="localhost", port=27017)
collection = db_manager.get_collection("users")
```

#### Connecting to PostgreSQL

```python
from auth_plugin.db_manager import DBManager

db_manager = DBManager(db_type="postgres", db_name="your_db_name", host="localhost", port=5432, user="your_username", password="your_password")
db_manager.execute_query("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(100))")
```

#### Connecting to MySQL

```python
from auth_plugin.db_manager import DBManager

db_manager = DBManager(db_type="mysql", db_name="your_db_name", host="localhost", port=3306, user="your_username", password="your_password")
db_manager.execute_query("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100))")

```

### 4. **Utility Functions**

The library also provides various utility functions that can be used across different modules:

```python
from auth_plugin.utils import hash_password, verify_password

hashed_password = hash_password("your_password")
is_correct = verify_password("your_password", hashed_password)
```

## Running Tests

To run the tests, ensure you're in the root directory and use the following command:

```bash
PYTHONPATH=. python -m unittest discover -s tests
```

This will run all the test cases in the `tests` directory.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

### Steps to Contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This library is inspired by common authentication needs in modern web applications.
- Special thanks to the contributors who helped improve this project.

## Contact

If you have any questions or suggestions, feel free to open an issue or reach out to [your email address].

### Customization

- Replace `yourusername` in the Git clone URL with your GitHub username.
- Replace `"your_secret_key"`, `"your_client_id"`, `"your_client_secret"`, etc., with actual values relevant to your application.
- Add any additional information that might be specific to your project.

This `README.md` provides a comprehensive guide to using your `auth-plugin` library, including installation, usage, testing, and contribution instructions.
