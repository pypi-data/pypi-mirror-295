__all__ = ["BaseProxyRotator"]

from abc import ABC, abstractmethod
from .schemas import ProxySchema
from .proxy_types import ProxyType
from typing import Optional


class BaseProxyRotator(ABC):
    @abstractmethod
    def rotate(self, old_proxy: Optional[ProxySchema], delete: bool = False, type: ProxyType = ProxyType.HTTP) -> str:
        """
        # Rotates the given proxy and returns a new proxy.

        :param old_proxy: Current proxy, not required, specified only when delete is True.
        :param delete: A flag indicating whether the old proxy should be deleted after rotation. Default is False.
        :param type: The type of proxy to return. Default is ProxyType.HTTP.
        :return: The new proxy as a string.
        """
        NotImplementedError()
    