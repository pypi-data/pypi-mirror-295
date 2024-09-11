
from setuptools import setup, find_packages

setup(
    name="mlflow-oidc-auth-siam",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-login",
        "flask-wtf",
        "werkzeug",
    ],
    entry_points={
        "console_scripts": [
            "auth=auth.cli:main",
        ],
    },
    author="Siam Rahman",
    author_email="siam.rahman@grabtaxi.com",
    description="An OIDC authentication package for MLFlow",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
