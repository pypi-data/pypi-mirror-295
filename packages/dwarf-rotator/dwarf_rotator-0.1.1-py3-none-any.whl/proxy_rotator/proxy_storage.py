__all__ = ["ProxyStorage"]

from .ProxyStorage import BaseProxyStorage
from .schemas import ProxySchema
from .proxy_types import ProxyType
from typing import List, Dict
import random
import logging


class ProxyStorage(BaseProxyStorage):
    def __init__(self, logger: logging.Logger) -> None:
        self.__proxy: Dict[ProxyType, List[ProxySchema]] = {}
        self.__deleted: int = 0
        self.__logger = logger

    def add(self, proxy: ProxySchema) -> None:
        if proxy.type not in self.__proxy:
            self.__proxy[proxy.type] = []

        self.__proxy[proxy.type].append(proxy)

    def get(self, type: ProxyType) -> ProxySchema:
        if type not in self.__proxy:
            raise KeyError(f"Key error [{type}]")

        if not self.__proxy[type]:
            raise ValueError(f"No proxies available for type")
        
        return random.choice(self.__proxy[type])

    def delete(self, proxy: ProxySchema) -> None:
        for i, current_proxy in enumerate(self.__proxy[proxy.type]):
            if current_proxy.ip_address == proxy.ip_address and current_proxy.port == proxy.port:
                self.__proxy[proxy.type].pop(i)
                self.__deleted += 1
                self.__logger.info(f"[🗑] {current_proxy.type}://{current_proxy.ip_address}:{current_proxy.port} deleted.")
                return True
        return False
    
    def __str__(self) -> str:
        lines = ["\n"]
        for key in self.__proxy.keys():
            lines.append(f"{key} - {len(self.__proxy[key])}")
        
        lines.append(f"🗑 deleted: {self.__deleted}\n")

        return f"\n".join(lines)
