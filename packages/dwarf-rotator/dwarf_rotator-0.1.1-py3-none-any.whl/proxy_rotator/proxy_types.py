__all__ = ["ProxyType"]

from enum import Enum


class ProxyType(str, Enum):
    HTTP = "http"
    HTTPS = "https"
