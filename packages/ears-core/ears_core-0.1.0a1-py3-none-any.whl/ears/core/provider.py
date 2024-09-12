from typing import Optional, Protocol

from .exceptions import NotSupportedError
from .models import MusicResource, Track, TrackSearchQuery
from .types import URN


class MusicProviderProtocol(Protocol):
    """ """

    name: str
    """ """

    def get_playlist(self, playlist_urn: URN) -> list[Track]:
        """ """
        pass

    def add_to_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        """ """
        pass

    def remove_from_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        """ """
        pass

    def search_track(self, query: TrackSearchQuery) -> list[Track]:
        """ """
        pass

    def parse_urn(self, urn: URN) -> MusicResource:
        """ """
        pass


class BaseMusicProvider(MusicProviderProtocol):
    """ """

    def get_playlist(self, playlist_urn: URN) -> list[Track]:
        raise NotSupportedError()

    def add_to_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        raise NotSupportedError()

    def remove_from_playlist(self, playlist_urn: URN, track_urn: URN) -> None:
        raise NotSupportedError()

    def search_track(self, query: TrackSearchQuery) -> list[Track]:
        raise NotSupportedError()

    def parse_urn(self, urn: Optional[str]) -> MusicResource:
        resource = MusicResource.from_urn(urn)
        if resource.provider != self.name:
            raise ValueError(
                f"Provider mismatch, expected {self.name},"
                f" got {resource.provider}"
            )
        return resource
