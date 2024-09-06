from setuptools import setup, find_packages

setup(
    name="auth-plugin",
    version="0.2.0",
    packages=find_packages(),
    install_requires=["PyJWT", "requests"],
    author="Visesh Agarwal",
    author_email="viseshagarwal@outlook.com",
    description="A simple plugin-based authentication library",
    license="MIT",
    url="https://github.com/viseshagarwal/auth-plugin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
