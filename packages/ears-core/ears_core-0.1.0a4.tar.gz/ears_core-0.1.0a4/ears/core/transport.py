from typing import Protocol, runtime_checkable

from .types import TransportClass


@runtime_checkable
class TransportFactory(Protocol):
    """
    A protocol for object that aims to create ready to use transport instance.
    Such transport can be either synchronous or asynchronous as client type
    is abstracted by `TransportClass` type var.
    """

    def create(self) -> TransportClass:
        """
        Create and return a transport instance.

        Returns
        -------
            TransportClass: A ready to be used transport instance.
        """
        pass
