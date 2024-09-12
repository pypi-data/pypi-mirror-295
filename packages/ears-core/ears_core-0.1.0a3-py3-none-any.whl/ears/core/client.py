from typing import Protocol

from .transport import TransportFactory
from .types import TransportClass


class ClientProtocol(Protocol):
    """
    A protocol for class that carries a transport to interact
    with an external API.
    """

    transport: TransportClass


class BaseClient(ClientProtocol):
    """
    A base implementation of client protocol
    """

    def __init__(
        self,
        transport_or_factory: TransportClass | TransportFactory,
    ) -> None:
        """
        A default constructor that handles transport managment.

        Args
        ----
            transport_or_factory (TransportClass | TransportFactory):
                Either a ready to use transport instance, or a factory
                instance that can be used to create the delegate transport.
        """
        if isinstance(transport_or_factory, TransportFactory):
            self.transport = transport_or_factory.create()
        else:
            self.transport = transport_or_factory
