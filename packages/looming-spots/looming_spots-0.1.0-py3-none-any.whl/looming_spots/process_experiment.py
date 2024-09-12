from pathlib import Path

from looming_spots.constants import RAW_DATA_DIRECTORY, PROCESSED_DATA_DIRECTORY
from lmtracker.track_mouse import process_behaviour


def get_mouse_ids():
    mouse_ids = ['1097633',
                 '1097634',
                 '1097635',
                 '1097639']

    return mouse_ids


mouse_ids = get_mouse_ids()


for m_id in mouse_ids:
    process_behaviour(m_id)


