from typing import Any, TypeVar

from httpx import Client
from pydantic import BaseModel

Event = dict[str, Any]
PydanticModelType = TypeVar("PydanticModelType", bound=BaseModel)
TransportClass = Client
URN = str
