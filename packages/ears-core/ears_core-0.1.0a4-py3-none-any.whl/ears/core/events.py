from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .types import URN


class PlaylistAction(str, Enum):
    """
    Enumeration of action that are available for a `PlaylistEvent`.
    """

    add = "add"
    """ Add a track to a playlist. """

    broadcast = "broadcast"
    """ Broadcast every track from a playlist. """

    remove = "remove"
    """ Remove a track from a playlist. """


class PlaylistEvent(BaseModel):
    """
    A `PlaylistEvent` describe an action to be executed
    for a target `Playlist`.
    """

    action: PlaylistAction
    """ A target action this event requires. """

    playlist: URN
    """ A target Playlist to apply required action to. """

    track: Optional[URN] = None
    """ An optional track to apply action to the playlist with. """
