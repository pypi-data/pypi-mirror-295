from typing import Any, Callable, TypeVar, Union

from httpx import Client
from pydantic import BaseModel

Event = dict[str, Any]

ProxyModelType = TypeVar(
    "ProxyModelType"
)  # , bound=...) # TODO: bound to base type.
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
PydanticEvent = Union[Event, BaseModel]

TransportClass = Client

URN = str

EventPublisherType = Callable[[Union[dict[str, Any], PydanticEvent]], None]
