__all__ = ["ProxyRotator"]

from .ProxyRotator import BaseProxyRotator
from .proxy_storage import ProxyStorage
from .proxy_types import ProxyType
from .schemas import ProxySchema
from typing import Optional
import logging


class ProxyRotator(BaseProxyRotator):
    def __init__(self, proxy_storage: ProxyStorage, logger: logging.Logger) -> None:
        self.__proxy_storage = proxy_storage
        self.__logger = logger 
        
    def rotate(self, old_proxy: Optional[ProxySchema] = None, delete: bool = False, type: ProxyType = ProxyType.HTTP) -> str:
        if delete:
            if old_proxy is None:
                raise ValueError("old_proxy must be not None")
            
            try:
                self.__proxy_storage.delete(old_proxy)
            except ValueError as e:
                self.__logger.error(f"Error deleting old proxy: {e}")
        
        try:
            new_proxy = self.__proxy_storage.get(type)
        except KeyError:
            raise ValueError(f"No proxies available for type [{type}]")

        return f"{new_proxy.ip_address}:{new_proxy.port}"
