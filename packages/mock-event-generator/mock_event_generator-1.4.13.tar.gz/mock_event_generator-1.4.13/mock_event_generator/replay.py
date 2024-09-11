"""Utilities for generating replay events."""

import itertools
import math
from typing import Iterator

from astropy.time import Time

from .gracedbs import GraceDBWithContext
from .models import SEventDescription


def calculate_offset(start: int, end: int, t_reference: float) -> float:
    """Calculate the replay offset based off of a reference time.

    Parameters:
        start: start time (GPS) of the replay.
        end: end time (GPS) of the replay.
        t_reference: reference time to calculate the offset for.

    Returns:
        The replay offset.
    """
    duration = end - start

    # determine offset needed for replay
    num_replays = math.floor((t_reference - start) / duration)
    return num_replays * duration


def replay_superevents(
    client: GraceDBWithContext, start: int, end: int
) -> Iterator[SEventDescription]:
    """Generate a continuous replay of superevents.

    This will query GraceDB for the times in question and yield
    results from the superevent query. The replay will cycle
    continuously.

    Parameters:
        client: the GraceDB client to query from.
        start: start time (GPS) of the replay.
        end: end time (GPS) of the replay.

    Yields:
        Superevent descriptions.
    """
    now = Time.now().gps
    offset = calculate_offset(start, end, now)

    # make two queries:
    #  1. from 'now' to end of replay
    #  2. from start of replay to 'now'
    to_end = client.superevents(
        query=f't_0: {now - offset} .. {end}',
        orderby='t_0',
    )
    from_start = client.superevents(
        query=f't_0: {start} .. {now - offset}',
        orderby='t_0',
    )

    # stitch the results of these two queries
    # to generate a continuous replay
    for sevent in itertools.cycle(itertools.chain(to_end, from_start)):
        yield SEventDescription(
            id=sevent['superevent_id'],
            source=client.meg_alias or client.meg_url,
            t_start=sevent['t_start'],
            t_0=sevent['t_0'],
            t_end=sevent['t_end'],
            gevent_ids=sevent['gw_events'],
        )
