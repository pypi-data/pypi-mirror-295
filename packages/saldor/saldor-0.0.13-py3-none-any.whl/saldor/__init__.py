# The existence of an __init__.py file allows users to import the directory as a regular package

from .saldor_client import (
    SaldorClient as SaldorClient,
)  # This is weird syntax, but it's demanded by mypy
