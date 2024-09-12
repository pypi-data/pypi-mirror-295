from typing import Any, Generic

from httpx import AsyncClient, Client

from .types import ProxyModelType, TransportClass, TransportType


class BaseProxy(Generic[TransportType, ProxyModelType]):
    """Base proxy class for client extension object."""

    transport: TransportClass

    def __init__(
        self,
        transport: TransportType,
        model: ProxyModelType,
    ) -> None:
        self.model = model
        self.transport = transport

    def __getattr__(self, attr: str) -> Any:
        # TODO: check if exist first.
        return getattr(self.model, attr)


class BaseClientProxy(BaseProxy[Client, ProxyModelType]):
    pass


class BaseAsyncClientProxy(BaseProxy[AsyncClient, ProxyModelType]):
    pass
