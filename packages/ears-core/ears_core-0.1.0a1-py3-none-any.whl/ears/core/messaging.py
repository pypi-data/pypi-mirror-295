from typing import Protocol, Type

from .types import Event, PydanticEvent, PydanticModel


class EventPublisher(Protocol):
    """
    Protocol for message publishing.
    """

    def publish(self, event: PydanticEvent) -> None:
        """ """
        pass


class EventPublisherFactory(Protocol):
    """ """

    def create(self, topic: str) -> EventPublisher:
        """ """
        pass


class EventReceiver(Protocol):
    """
    Protocol for message handling.
    """

    def receive(
        self,
        event: Event,
        model: Type[PydanticModel],
    ) -> PydanticModel:
        """ """
        pass
