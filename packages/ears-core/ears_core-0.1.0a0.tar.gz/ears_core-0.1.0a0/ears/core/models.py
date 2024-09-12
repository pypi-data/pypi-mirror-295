from typing import Any, Optional

from pydantic import AnyHttpUrl, BaseModel

from .types import URN, MusicResourceType


class MusicResource(BaseModel):
    id: Any
    provider: str
    type: MusicResourceType
    url: Optional[AnyHttpUrl] = None

    @classmethod
    def from_urn(cls, urn: Optional[URN]) -> "MusicResource":
        """
        Parse the given URN into a target MusicResource.
        Such URN are designed as follow:

        urn:PROVIDER:TYPE:IDENTIFIER

        Where given provider should match this object target.
        """
        if urn is None:
            raise ValueError()
        tokens = urn.split(":")
        if len(tokens) != 4 or tokens[0] != "urn":
            raise ValueError(f"Invalid urn {urn}")
        return MusicResource(
            id=tokens[3],
            provider=tokens[1],
            type=tokens[2],  # type: ignore
        )

    def to_urn(self) -> URN:
        return f"urn:{self.provider}:{self.type}:{self.id}"


class TrackSearchQuery(BaseModel):
    album: str
    artist: str
    title: str


class TrackMetadata(TrackSearchQuery):
    cover: AnyHttpUrl
    preview: Optional[AnyHttpUrl] = None


class Track(BaseModel):
    metadata: TrackMetadata
    resource: MusicResource


class TrackMatching(BaseModel):
    origin: MusicResource
    destination: MusicResource
    metadata: Optional[TrackMetadata] = None
