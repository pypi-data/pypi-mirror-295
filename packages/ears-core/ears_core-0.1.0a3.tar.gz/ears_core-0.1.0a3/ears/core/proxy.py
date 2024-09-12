from typing import Any, Generic


from .types import ProxyModelType, TransportClass


class BaseProxy(Generic[ProxyModelType]):
    """Base proxy class for client extension object."""

    transport: TransportClass

    def __init__(
        self,
        transport: TransportClass,
        model: ProxyModelType,
    ) -> None:
        self.model = model
        self.transport = transport

    def __getattr__(self, attr: str) -> Any:
        # TODO: check if exist first.
        return getattr(self.model, attr)


class BaseClientProxy(BaseProxy[ProxyModelType]):
    pass
