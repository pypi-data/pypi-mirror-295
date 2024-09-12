import pathlib
import warnings
from pathlib import Path
from shutil import copyfile

import looming_spots.util

from looming_spots.db.session import Session
from looming_spots.exceptions import MouseNotFoundError
from looming_spots.util import generic_functions


def load_sessions(mouse_id, processed_data_directory):
    processed_dir = Path(processed_data_directory)
    mouse_directory = processed_dir / mouse_id
    print(f"loading.... {mouse_directory}")
    session_list = []
    if mouse_directory.exists():

        for s in mouse_directory.rglob("**/"):

            if s.exists():

                file_names = [f"{x.stem}{x.suffix}" for x in list(s.glob("*"))]
                # print(file_names)
                if not contains_analog_input(file_names):
                    continue

                if "contrasts.mat" not in file_names:
                    print("no contrasts mat")

                    if not s.exists():
                        continue

                    if not looming_spots.util.generic_functions.is_datetime(s.stem):
                        print("not datetime, skipping")
                        continue

                    if not contains_video(file_names) and not contains_tracks(
                        s
                    ):
                        warnings.warn("This mouse has no tracks")
                        # if not get_tracks_from_raw(
                        #     str(mouse_directory).replace("derivatives", "raw_data")
                        # ):
                        #     continue

            ses = Session(path=s, mouse_id=mouse_id)
            session_list.append(ses)

        if len(session_list) == 0:
            msg = f"the mouse: {mouse_id} has not been processed or perhaps the mouse id is wrong"
            raise MouseNotFoundError(msg)

        return sorted(session_list)
    msg = f"the mouse: {mouse_id} has not been copied to the processed data directory"
    warnings.warn(msg)

    raise MouseNotFoundError()


def contains_analog_input(file_names):
    if "AI.bin" in file_names or "AI.tdms" in file_names or 'analog.bin' in file_names:
        return True
    return False


def contains_video(file_names):
    return any(".avi" in fname for fname in file_names) or any(
        ".mp4" in fname for fname in file_names
    )


def contains_tracks(session_directory):
    p = pathlib.Path(session_directory)
    if len(list(p.rglob("dlc_x_tracks.npy"))) == 0:
        return False
    else:
        return True


def get_tracks_from_raw(directory):
    print(f"getting tracks from {directory}")
    p = Path(directory)
    track_paths = p.rglob("*tracks.npy")
    if len(list(p.rglob("*tracks.npy"))) == 0:
        print("no track paths found...")
        return False

    for tp in track_paths:
        raw_path = str(tp)
        processed_path = raw_path.replace("raw_data", "processed_data")
        print(f"copying {raw_path} to {processed_path}")
        copyfile(raw_path, processed_path)
    return True
