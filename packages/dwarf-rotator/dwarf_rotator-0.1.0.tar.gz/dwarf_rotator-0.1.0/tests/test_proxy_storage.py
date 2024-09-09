import pytest
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


def test_add(proxy_storage):
    proxy = ProxySchema(ip_address="192.168.1.1", port=8080, type=ProxyType.HTTP)
    proxy_storage.add(proxy)
    assert len(proxy_storage._ProxyStorage__proxy[ProxyType.HTTP]) == 1


def test_get(proxy_storage):
    proxy1 = ProxySchema(ip_address="192.168.1.1", port=8080, type=ProxyType.HTTP)
    proxy2 = ProxySchema(ip_address="192.127.2.32", port=3232, type=ProxyType.HTTP)
    proxy3 = ProxySchema(ip_address="128.255.9.29", port=3602, type=ProxyType.HTTP)

    proxy_storage.add(proxy1)
    proxy_storage.add(proxy2)
    proxy_storage.add(proxy3)

    result = proxy_storage.get(type=ProxyType.HTTP)
    assert result in [proxy1, proxy2, proxy3]


def test_delete(proxy_storage):
    proxy = ProxySchema(ip_address="192.168.1.1", port=8080, type=ProxyType.HTTP)
    proxy_storage.add(proxy)
    result = proxy_storage.delete(proxy)
    assert result is True
    assert len(proxy_storage._ProxyStorage__proxy[ProxyType.HTTP]) == 0


def test_str_method(proxy_storage):
    proxy = ProxySchema(ip_address="192.168.1.1", port=8080, type=ProxyType.HTTP)
    proxy_storage.add(proxy)
    result = str(proxy_storage)
    assert "HTTP - 1" in result
    assert "🗑 deleted: 0" in result
