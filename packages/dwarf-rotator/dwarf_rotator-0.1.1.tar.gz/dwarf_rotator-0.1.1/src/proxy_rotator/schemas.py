__all__ = ["ProxySchema"]

from pydantic import BaseModel, IPvAnyAddress, conint
from typing import Annotated
from .proxy_types import ProxyType


class ProxySchema(BaseModel):
    type: ProxyType
    ip_address: IPvAnyAddress
    port: Annotated[int, conint(ge=1024, le=65535)]
