import os

import numpy as np
import pandas as pd
import scipy.signal

import looming_spots.util.video_processing

from daq_loader.load import load_all_channels_on_clock_ups
from looming_spots.exceptions import PdTooShortError


class NoPdError(Exception):
    pass


def get_test_looms_from_loom_idx(loom_idx, n_looms_per_stimulus=5):
    if not contains_lse(loom_idx, n_looms_per_stimulus):
        return loom_idx[::n_looms_per_stimulus]
    else:
        test_loom_idx = get_test_loom_idx(loom_idx, n_looms_per_stimulus)
        return loom_idx[test_loom_idx]


def get_test_loom_idx(
    loom_idx, n_looms_per_stimulus=5
):  # WARNING: THIS DOES NOT DO WHAT THE USER EXPECTS
    if contains_lse(loom_idx):
        loom_burst_onsets = np.diff(loom_idx[::n_looms_per_stimulus])
        min_ili = min(loom_burst_onsets)
        print("min_ili: {min_ili}")
        test_loom_idx = np.where(loom_burst_onsets > min_ili + 200)[0] + 1
        return test_loom_idx * n_looms_per_stimulus


def get_test_looms_from_photodiode_trace(directory, photometry=True):
    loom_idx, _ = get_loom_idx_from_photodiode_trace(directory,photometry)
    return get_test_looms_from_loom_idx(loom_idx)


def get_loom_idx_from_photodiode_trace(directory, save=True, photometry=True):
    try:
        data = load_all_channels_on_clock_ups(directory)
        photodiode_trace = pd.Series(data["photodiode"])

        print(len(photodiode_trace))
        #
        # loom_starts, loom_ends = find_pd_threshold_crossings(photodiode_trace)
        loom_starts = np.where(np.diff(photodiode_trace.ewm(span=4).mean()>0.4))[0][::2]-1
        loom_ends = np.where(np.diff(photodiode_trace.ewm(span=4).mean()>0.4))[0][1::2]-1

    except NoPdError as e:
        print(e)
        loom_starts = []
        loom_ends = []

    except PdTooShortError as e:
        print(e)
        loom_starts = []
        loom_ends = []

    dest = os.path.join(directory, "loom_starts.npy")
    if save:
        np.save(dest, loom_starts)
    return loom_starts, loom_ends


def get_lse_loom_idx(idx, n_looms_per_stimulus=5):
    if contains_lse(idx, n_looms_per_stimulus):
        onsets_diff = np.diff(idx[::n_looms_per_stimulus])
        min_ili = min(onsets_diff)
        loom_idx_lse = np.where(onsets_diff < min_ili + 150)[
            0
        ]  # FIXME: this value is chosen for.. reasons
        loom_idx_lse = np.concatenate(
            [loom_idx_lse, [max(loom_idx_lse) + 1]]
        )  # adds last loom as ILI will always be bigger
        return idx[loom_idx_lse * n_looms_per_stimulus]


def get_lse_start(loom_idx, n_looms_per_stimulus=5):
    return get_lse_loom_idx(loom_idx, n_looms_per_stimulus)[0]


def contains_lse(loom_idx, n_looms_per_stimulus=5):
    if not loom_idx.shape:
        return False
    ili = np.diff(np.diff(loom_idx[::n_looms_per_stimulus]))
    if np.count_nonzero([np.abs(x) < 5 for x in ili]) >= 3:
        return True
    return False


def get_nearest_clock_up(raw_pd_value, clock_ups_pd):
    from bisect import bisect_left

    insertion_point = bisect_left(clock_ups_pd, raw_pd_value)
    difference_left = raw_pd_value - clock_ups_pd[insertion_point - 1]
    difference_right = raw_pd_value - clock_ups_pd[insertion_point]

    increment = 0 if difference_right < difference_left else -1
    nearest_clock_up_idx = insertion_point + increment
    distance_from_clock_up = (
        difference_left
        if abs(difference_left) < abs(difference_right)
        else difference_right
    )

    return nearest_clock_up_idx, distance_from_clock_up


def find_pd_threshold_crossings(ai, threshold=0.4):

    filtered_pd = filter_pd(ai)

    if not (filtered_pd > threshold).any():
        return [], []

    threshold = np.median(filtered_pd) + np.nanstd(filtered_pd) * 3  # 3
    print(f"threshold: {threshold}")
    loom_on = (filtered_pd > threshold).astype(int)
    loom_ups = np.diff(loom_on) == 1
    loom_starts = np.where(loom_ups)[0]
    loom_downs = np.diff(loom_on) == -1
    loom_ends = np.where(loom_downs)[0]
    return loom_starts, loom_ends


def filter_pd(pd_trace, fs=10000):  # 10000
    b1, a1 = scipy.signal.butter(3, 1000.0 / fs * 2.0, "low")
    pd_trace = scipy.signal.filtfilt(b1, a1, pd_trace)
    return pd_trace


def get_auditory_onsets_from_auditory_trace(directory, save=True):
    aud = pd.Series(load_all_channels_on_clock_ups(directory)["auditory_stimulus"])
    stimulus=(aud.ewm(span=20).std()-aud.ewm(span=20).std().mean())
    stimulus[:500] = np.median(stimulus)
    stimulus[-500:] = np.median(stimulus)
    thresh = 0.3 #np.std(stimulus)*5
    stim_above_thresh = stimulus>thresh
    auditory_onsets = np.where(np.diff(stim_above_thresh.astype(int))>0)[0]
    dest = os.path.join(directory, "auditory_starts.npy")

    if save:
        np.save(dest, auditory_onsets)
    return auditory_onsets


def manually_correct_ai(directory, start, end):
    """
    This is useful when there are clear errors in the photodiode (e.g. if the photodiode is removed during the experiment
    and allows the user to replace chunks of the processed photodiode trace with the median baseline so it doesn't
    interfere with stimulus detection

    :param directory:
    :param start:
    :param end:
    :return:
    """
    photodiode_trace = load_all_channels_on_clock_ups(directory)["photodiode"]
    photodiode_trace[start:end] = np.median(photodiode_trace)
    save_path = os.path.join(directory, "AI_corrected")
    np.save(save_path, photodiode_trace)


def auto_fix_ai(
    directory, n_samples_to_replace=500, screen_off_threshold=0.02
):
    """
    Automatically attempts to correct photodiode errors, but safer to use manually_correct_ai

    :param directory:
    :param n_samples_to_replace:
    :param screen_off_threshold:
    :return:
    """

    photodiode_trace = load_all_channels_on_clock_ups(directory)["photodiode"]
    screen_off_locs = np.where(photodiode_trace < screen_off_threshold)[
        0
    ]  # TODO: remove hard var

    if len(screen_off_locs) == 0:
        return

    start = screen_off_locs[0]
    end = start + n_samples_to_replace
    photodiode_trace[start:end] = np.median(photodiode_trace)
    save_path = os.path.join(directory, "AI_corrected")
    np.save(save_path, photodiode_trace)
    auto_fix_ai(directory, n_samples_to_replace=n_samples_to_replace)
