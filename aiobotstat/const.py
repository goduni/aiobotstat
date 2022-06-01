"""Constant dataclasses."""

from enum import Enum


class HTTPMethods(str, Enum):
    """Available HTTP methods."""

    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"
