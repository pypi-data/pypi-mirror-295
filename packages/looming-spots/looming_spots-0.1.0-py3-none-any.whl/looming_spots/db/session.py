import os
import pathlib
import warnings
from datetime import datetime

import numpy as np
import skvideo.io
from cached_property import cached_property
from looming_spots.analyse import tracks
from looming_spots.analyse.tracks import get_tracking_method
from looming_spots.constants import AUDITORY_STIMULUS_CHANNEL_ADDED_DATE
from looming_spots.db import trial
from daq_loader import load
from looming_spots.loom_io import photodiode

from looming_spots.util import generic_functions


class Session(object):

    """
    The Session class aims to load data that has been acquired in a series of recording sessions and provide
    a simple means to read and access this data, trials are generated from this data and have access to the data
    provided.

    """

    def __init__(
        self,
        path,
        mouse_id=None,
        n_looms_to_view=0,
        n_lse_looms=120,
        n_trials_to_include=3,
    ):
        self.path = path
        self.dt = datetime.strptime(self.path.stem, "%Y%m%d_%H_%M_%S")
        self.mouse_id = mouse_id
        self.n_looms_to_view = n_looms_to_view
        self.n_lse_looms = n_lse_looms
        self.n_trials_to_include = n_trials_to_include
        self.next_session = None
        self.previous_session = None

    @property
    def frame_rate(self):
        """
        The camera frame rate is controlled by a clock TTL pulse that is recorded along with all the other data, and this
        clock can be used to infer the frame rate used.

        :return:
        """
        p = pathlib.Path(self.path)
        frame_rate_file_exists = len(list(p.glob("frame_rate.npy"))) == 1

        if frame_rate_file_exists:
            frame_rate = np.load(str(p / "frame_rate.npy"))
        else:
            if "AI.tdms" in os.listdir(self.path):
                clock = self.get_clock_raw()
                clock_ups = load.get_clock_ups(clock)
                if np.nanmedian(np.diff(clock_ups)) == 333:
                    frame_rate = 30
                elif np.nanmedian(np.diff(clock_ups)) == 200:
                    frame_rate = 50
                elif np.nanmedian(np.diff(clock_ups)) == 100:
                    frame_rate = 100
                else:
                    frame_rate = 30
            else:
                frame_rate = 30
            np.save(str(p / "frame_rate.npy"), frame_rate)

        return frame_rate

    def __len__(self):
        return len(self.data["photodiode"])

    def __lt__(self, other):
        """
        Allows sorting trials chronologically

        :param other:
        :return:
        """
        return self.dt < other.dt

    def __gt__(self, other):
        """
        Allows sorting trials chronologically

        :param other:
        :return:
        """
        return self.dt > other.dt

    def __add__(self, a):
        for t in self.trials:
            t + a

    def directory(self, processed_data_directory):
        return os.path.join(processed_data_directory, self.mouse_id)


    @property
    def video_path(self):
        return os.path.join(
            self.path.replace("processed_data", "raw_data"), "camera.avi"
        )

    @property
    def parent_path(self):
        return os.path.split(self.path)[0]

    @cached_property
    def loom_paths(self):
        paths = []

        if self.n_looms == 0:
            print(f"no looms in {self.path}")
            return []

        for name in os.listdir(self.path):
            loom_folder = os.path.join(self.path, name)
            if os.path.isdir(loom_folder) and "loom" in name:
                paths.append(loom_folder)

        if len(paths) == 0:
            warnings.warn(f"no loom folder paths, please check you have tracked this session: {msg}")
            return []
            #raise LoomsNotTrackedError(self.path)

        loom_indices = [int(path[-1]) for path in paths]
        sorted_paths, idx = generic_functions.sort_by(
            paths, loom_indices, descend=False
        )

        return sorted_paths

    def contains_auditory(self):
        aud_idx_path = os.path.join(self.path, "auditory_starts.npy")
        if os.path.isfile(aud_idx_path):
            if len(np.load(aud_idx_path)) > 0:
                return True

        recording_date = datetime.strptime(
            os.path.split(self.path)[-1], "%Y%m%d_%H_%M_%S"
        )

        if "AI.tdms" in os.listdir(self.path):
            return True

        if recording_date > AUDITORY_STIMULUS_CHANNEL_ADDED_DATE:
            ad = load.load_all_channels_on_clock_ups(
                self.path
            )["auditory_stimulus"]
            if (ad > 0.7).any():
                return True

    @cached_property
    def trials(self):
        visual_trials_idx = self.get_looming_stimuli_test_trials_idx()
        auditory_trials_idx = self.get_auditory_trials_idx()
        visual_trials = self.initialise_trials(
            visual_trials_idx,
            "visual",
        )
        auditory_trials = self.initialise_trials(
            auditory_trials_idx,
            "auditory",
        )

        return sorted(visual_trials + auditory_trials)

    def initialise_trials(self, idx, stimulus_type):
        if idx is not None:
            if len(idx) > 0:
                trials = []
                for i, onset_in_samples in enumerate(idx):
                    if stimulus_type == "visual":
                        t = trial.VisualStimulusTrial(
                            self,
                            directory=self.path,
                            sample_number=onset_in_samples,
                            trial_type=self.get_trial_type(onset_in_samples),
                            stimulus_type="loom",
                        )
                    elif stimulus_type == "auditory":
                        t = trial.AuditoryStimulusTrial(
                            self,
                            directory=self.path,
                            sample_number=onset_in_samples,
                            trial_type=self.get_trial_type(onset_in_samples),
                            stimulus_type="auditory",
                        )

                    else:
                        raise NotImplementedError

                    trials.append(t)
                return trials
            else:
                return []
        return []

    def get_trials_of_protocol_type(self, key):
        """
        Returns trials grouped as either belonging to an LSE protocol, or being a testing trial of some sort
        to later be more specifically classified as a pre- or post- lse testing trial.

        :param key:
        :return:
        """
        if key == "test":
            return [t for t in self.trials if "test" in t.trial_type]

        return [t for t in self.trials if t.trial_type == key]

    @property
    def trials_results(self):
        """

        :return:
        """
        test_trials = [t for t in self.trials if "test" in t.trial_type]
        return np.array(
            [
                t.track.classify_escape()
                for t in test_trials[: self.n_trials_to_include]
            ]
        )

    @property
    def n_trials_total(self):
        return len(self.trials)

    @property
    def n_test_trials(self):
        return len(self.get_trials_of_protocol_type("test"))

    @property
    def n_lsie_trials(self):
        return len(self.get_trials_of_protocol_type("lsie"))

    def hours(self):
        return self.dt.hour + self.dt.minute / 60

    @property
    def n_flees(self):
        return np.count_nonzero(self.trials_results)

    @property
    def n_non_flees(self):
        n_trials = len(self.trials_results)
        return n_trials - np.count_nonzero(self.trials_results)

    @property
    def n_looms(self):
        return len(self.looming_stimuli_idx)

    def get_reference_frame(self, idx=0):
        import skvideo.io

        vid = skvideo.io.vreader(self.video_path)
        for i, frame in enumerate(vid):
            if i == idx:
                return frame

    @property
    def photodiode_trace(self, raw=False):
        if raw:
            pd = load_all_channels_raw(self.path)["photodiode"]
        else:
            pd = self.data["photodiode"]
        return pd

    def get_clock_raw(self):
        return load_all_channels_raw(self.path)["clock"]

    @property
    def auditory_trace(self):
        return self.data["auditory_stimulus"]

    @cached_property
    def signal(self):
        if "signal" in self.data:
            return self.data["signal"]

    @cached_property
    def background(self):
        if "background" in self.data:
            return self.data["background"]

    @cached_property
    def data(self):
        return load.load_all_channels_on_clock_ups(self.path)

    @property
    def contains_lsie(self):
        return photodiode.contains_lse(self.looming_stimuli_idx)

    @cached_property
    def looming_stimuli_idx(self):
        loom_idx_path = os.path.join(self.path, "loom_starts.npy")
        if not os.path.isfile(loom_idx_path):
            _ = photodiode.get_loom_idx_from_photodiode_trace(
                self.path, save=True
            )[0]
        return np.load(loom_idx_path)

    @cached_property
    def auditory_stimuli_idx(self):
        if self.contains_auditory():
            aud_idx_path = os.path.join(self.path, "auditory_starts.npy")
            if not os.path.isfile(aud_idx_path):
                _ = photodiode.get_auditory_onsets_from_auditory_trace(
                    self.path, save=True
                )
            return np.load(aud_idx_path)

    def get_trial_type(self, onset_in_samples):
        if self.lse_idx is None:
            return "test"
        elif onset_in_samples in self.lse_idx:
            return "lse"
        else:
            return "test"

    @property
    def lse_idx(self):
        if self.contains_auditory():
            if photodiode.contains_lse(self.auditory_stimuli_idx, 1):
                return photodiode.get_lse_loom_idx(self.auditory_stimuli_idx, 1)

        if photodiode.contains_lse(self.looming_stimuli_idx, 5):
            return photodiode.get_lse_loom_idx(self.looming_stimuli_idx, 5)

    @property
    def lse_loom_idx(self):
        return photodiode.get_lse_loom_idx(self.looming_stimuli_idx)

    @property
    def test_loom_idx(self):
        return photodiode.get_test_looms_from_loom_idx(
            self.looming_stimuli_idx
        )

    @property
    def lsie_protocol_start(self):
        return photodiode.get_lse_start(self.looming_stimuli_idx)

    def test_loom_classification(self):  # TEST
        assert len(self.lsie_loom_idx) + len(self.test_loom_idx) == int(
            len(self.looming_stimuli_idx) / 5
        )

    def extract_peristimulus_videos_for_all_trials(self):
        for t in self.trials:
            t.extract_video()

    def contains_visual_stimuli(self):
        photodiode_trace = load_all_channels_on_clock_ups(self.path)[
            "photodiode"
        ]
        if (photodiode_trace > 0.5).any():
            return True

    def get_looming_stimuli_test_trials_idx(self):
        return self.looming_stimuli_idx[::5]

    def get_auditory_trials_idx(self):
        return self.auditory_stimuli_idx

    def get_data(self, key):
        data_func_dict = {
            "photodiode": self.get_photodiode_trace,
            "x_pos": self.x_pos,
            "y_pos": self.y_pos,
            "delta_f": self.get_delta_f,
            "loom_onsets": self.get_loom_idx,
            "auditory_onsets": self.get_auditory_idx,
            "trials": self.get_session_trials,
        }

        return data_func_dict[key]

    def get_photodiode_trace(self):
        return self.photodiode_trace - np.median(self.photodiode_trace)

    @cached_property
    def track(self):
        return tracks.track_in_standard_space(
            self.path, get_tracking_method(self.path), 0, len(self), save=True
        )

    def x_pos(self):
        return self.track[0]

    def y_pos(self):
        return self.track[1]

    def get_delta_f(self):
        return self.data["delta_f"]

    def get(self, key):
        current_session = self
        prev_samples = 0

        selection_dict = {
            "loom_idx": self.looming_stimuli_idx,
            "auditory_idx": self.auditory_stimuli_idx,
            "trials": self.trials,
        }

        while current_session is not None:
            print(f"prev_samples: {prev_samples}")
            current_session = current_session.previous_session
            if current_session is not None:
                prev_samples += len(current_session)

        if key == "trials":
            self + prev_samples
            return self.trials

        return selection_dict[key] + prev_samples

    def get_loom_idx(self):
        return self.get("loom_idx")

    def get_auditory_idx(self):
        return self.get("auditory_idx")

    def get_session_trials(self):
        return self.get("trials")

    @classmethod
    def set_next_session(cls, self, other):
        if self.next_session is None:
            print(f"setting next session for {self.path} to {other.path}")
            setattr(self, "next_session", other)

    @classmethod
    def set_previous_session(cls, self, other):
        if self.previous_session is None:
            print(f"setting previous session for {self.path} to {other.path}")
            setattr(self, "previous_session", other)

    def time_to_ephys(self, camera_frame_number, ephys_timestamps):
        return ephys_timestamps[camera_frame_number]
