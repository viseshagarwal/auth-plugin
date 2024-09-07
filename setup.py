from setuptools import setup, find_packages

setup(
    name="auth-plugin",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "PyJWT",
        "pymongo",
        "SQLAlchemy",
        "mysql-connector-python",
        "requests",
        "psycopg2",
        "cryptography",
        "certifi",
        "cffi",
    ],
    author="Visesh Agarwal",
    description="A robust Python library for JWT, OAuth2, and database authentication.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/viseshagarwal/auth-plugin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
