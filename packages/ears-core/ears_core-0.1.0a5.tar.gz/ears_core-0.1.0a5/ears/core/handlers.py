from .events import PlaylistAction, PlaylistEvent
from .messaging import EventPublisherFactory, EventReceiver
from .models import Track, TrackMatching
from .provider import MusicProviderProtocol
from .types import Event


def on_broadcast_playlist_event(
    provider: MusicProviderProtocol,
    event: Event,
    event_publisher_factory: EventPublisherFactory,
    event_receiver: EventReceiver,
    destination: str,
) -> None:
    """ """
    event_publisher = event_publisher_factory.create(destination)
    playlist_event = event_receiver.receive(event, PlaylistEvent)
    tracks = provider.get_playlist(playlist_event.playlist)
    for track in tracks:
        event_publisher.publish(track)


def on_update_playlist_event(
    provider: MusicProviderProtocol,
    event: Event,
    event_receiver: EventReceiver,
) -> None:
    """ """
    playlist_event = event_receiver.receive(event, PlaylistEvent)
    if playlist_event.action == PlaylistAction.add:
        if playlist_event.track is None:
            raise ValueError()
        provider.add_to_playlist(
            playlist_event.playlist,
            playlist_event.track,
        )
    elif playlist_event.action == PlaylistAction.remove:
        if playlist_event.track is None:
            raise ValueError()
        provider.remove_from_playlist(
            playlist_event.playlist,
            playlist_event.track,
        )


def on_search_track_event(
    provider: MusicProviderProtocol,
    event: Event,
    event_publisher_factory: EventPublisherFactory,
    event_receiver: EventReceiver,
    destination: str,
) -> None:
    """ """
    event_publisher = event_publisher_factory.create(destination)
    query = event_receiver.receive(event, Track)
    results = provider.search_track(query.metadata)
    if len(results) == 0:
        # TODO: figure out what to do here ?
        return
    event_publisher.publish(
        TrackMatching(
            origin=query.resource,
            destination=results[0].resource,
            metadata=results[0].metadata,
        )
    )
