__all__ = ["BaseProxyStorage"]

from abc import ABC, abstractmethod
from .proxy_types import ProxyType
from .schemas import ProxySchema


class BaseProxyStorage(ABC):
    """
    # Abstract class for storing and managing proxies

    This class defines the interface for storing proxies, retrieving proxies by type, and deleting proxies.
    Concrete implementations of this class should provide the actual mechanisms for working with proxy schemas.
    """
    @abstractmethod
    def add(self, proxy: ProxySchema) -> None:
        """
        # Adds a new proxy to the storage.

        :param proxy: The proxy schema containing information about the proxy to be added.
        """
        NotImplementedError()

    @abstractmethod
    def get(self, type: ProxyType) -> ProxySchema:
        """
        # Returns a random proxy

        :param type: The type of proxy to retrieve. This value should match one of the allowed proxy types defined in ProxyType.
        :return: The proxy schema corresponding to the specified type.
        """
        NotImplementedError()

    @abstractmethod
    def delete(self) -> bool:
        """
        # Deletes a proxy from the storage.
        
        :return: True if the proxy was successfully deleted, otherwise False."""
        NotImplementedError()
