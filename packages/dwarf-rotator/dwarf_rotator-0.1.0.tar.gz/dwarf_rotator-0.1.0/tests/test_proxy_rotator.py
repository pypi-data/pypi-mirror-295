import pytest
from src.proxy_rotator.proxy_rotator import ProxyRotator
from src.proxy_rotator.proxy_storage import ProxyStorage
from src.proxy_rotator.schemas import ProxySchema
from src.proxy_rotator.proxy_types import ProxyType
import logging

@pytest.fixture
def logger():
    return logging.getLogger("test_logger")

@pytest.fixture
def proxy_storage(logger):
    return ProxyStorage(logger)

@pytest.fixture
def proxy_rotator(proxy_storage, logger):
    return ProxyRotator(proxy_storage, logger)

def test_rotate(proxy_rotator, proxy_storage):
    proxy = ProxySchema(ip_address="192.168.1.1", port=8080, type=ProxyType.HTTP)
    proxy_storage.add(proxy)
    new_proxy = ProxySchema(ip_address="192.168.1.2", port=8081, type=ProxyType.HTTP)
    proxy_storage.add(new_proxy)
    result = proxy_rotator.rotate(type=ProxyType.HTTP)
    assert result in ["192.168.1.1:8080", "192.168.1.2:8081"]

def test_rotate_with_deletion(proxy_rotator, proxy_storage):
    proxy1 = ProxySchema(ip_address="192.168.1.1", port=8080, type=ProxyType.HTTP)
    proxy2 = ProxySchema(ip_address="255.255.255.255", port=8080, type=ProxyType.HTTP)

    proxy_storage.add(proxy1)
    proxy_storage.add(proxy2)

    result = proxy_rotator.rotate(old_proxy=proxy1, delete=True, type=ProxyType.HTTP)
    assert result != "192.168.1.1:8080"

def test_rotate_without_old_proxy(proxy_rotator):
    with pytest.raises(ValueError, match="old_proxy must be not None"):
        proxy_rotator.rotate(delete=True)

def test_rotate_no_proxies(proxy_rotator, proxy_storage):
    with pytest.raises(ValueError, match="No proxies available for type"):
        proxy_rotator.rotate(type=ProxyType.HTTP)
