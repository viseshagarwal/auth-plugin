# Contributing to Auth-Plugin Library

We welcome contributions to our Auth Plugin Library! Whether you're fixing a bug, adding new features, or improving documentation, your efforts are greatly appreciated. Follow the guidelines below to help make the process smooth for everyone.

## Getting Started

### 1. Fork the Repository

Start by forking the repository to your own GitHub account. This will create a copy of the repository under your GitHub account.

### 2. Clone the Repository

Clone the forked repository to your local machine:

```bash
git clone https://github.com/viseshagarwal/auth-plugin.git
cd auth-plugin
```

### 3. Set Up the Development Environment

Create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 4. Run Tests

Before making any changes, ensure that all tests pass:

```bash
python -m unittest discover tests
```

## Making Changes

### 1. Create a New Branch

Create a new branch for your changes. Use a descriptive name for your branch:

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Make the necessary changes in your branch. Please ensure that your code follows the project's coding standards.

### 3. Add Tests

If you're adding new functionality or fixing a bug, add corresponding test cases to ensure that your changes work as expected.

### 4. Run Tests

After making your changes, run the tests again to ensure everything works correctly:

```bash
python -m unittest discover tests
```

### 5. Commit Your Changes

Commit your changes with a clear and concise commit message:

```bash
git add .
git commit -m "Description of the changes made"
```

### 6. Push Your Changes

Push your changes to your forked repository:

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

Go to the original repository on GitHub and create a pull request. Describe your changes and link any relevant issues.

## Code Style

- Follow [PEP 8](https://pep8.org/) for Python code style.
- Write clear and concise commit messages.
- Ensure that your code is well-documented, especially for new features.

## Reporting Issues

If you encounter any issues or bugs, please [open an issue](https://github.com/your-username/auth-plugin/issues) on GitHub. Provide as much detail as possible, including steps to reproduce the issue.

## Code of Conduct

Please note that this project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Thank You!

Thank you for considering contributing to our project! Your support helps improve the library for everyone.
