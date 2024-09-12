import matplotlib.colors
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt, patches as patches

from matplotlib.collections import LineCollection
from looming_spots.constants import LOOM_ONSETS, NORMALISED_SHELTER_FRONT


def plot_looms(fig):
    for ax in fig.axes:
        for loom in [create_loom_patch(stim) for stim in LOOM_ONSETS]:
            ax.add_patch(loom)
    return fig


def plot_looms_upsampled(fig):
    for ax in fig.axes:
        for loom in [
            create_loom_patch(
                stim * 10000 / 30, upsample_factor=int(10000 / 30)
            )
            for stim in LOOM_ONSETS
        ]:
            ax.add_patch(loom)
    return fig


def plot_upsampled_looms_ax(ax=None):
    if ax is None:
        ax = plt.gca()
    looms = [
        create_loom_patch(stim * 10000 / 30, upsample_factor=int(10000 / 30))
        for stim in LOOM_ONSETS
    ]
    for loom in looms:
        ax.add_patch(loom)


def plot_stimulus(fig, onset=200, n_samples=90):
    for ax in fig.axes:
        patch = patches.Rectangle(
            (onset, -0.2), n_samples, 1.3, alpha=0.1, color="b", linewidth=0
        )
        ax.add_patch(patch)
    return fig


def plot_shelter_location(fig, context):
    for ax in fig.axes:
        plt.sca(ax)
        house_front = NORMALISED_SHELTER_FRONT
        plt.axhline(house_front, 0, 400, ls="--")


def plot_looms_ax(
    ax=None,
    vertical=True,
    height=1.3,
    loom_n_samples=14,
    relative=False,
    upsample_factor=1,
    type='line',
):
    if ax is None:
        ax = plt.gca()
    loom_onsets = LOOM_ONSETS
    if relative:
        loom_onsets = [x - 200 for x in loom_onsets]

    if type == 'line':
        [plt.axvline(x, color="k", linestyle="--", zorder=0) for x in (loom_onsets)]
    else:
        looms = [
            create_loom_patch(
                stim,
                vertical=vertical,
                height=height,
                loom_n_samples=loom_n_samples,
                upsample_factor=upsample_factor,
            )
            for stim in loom_onsets
        ]
        for loom in looms:
            ax.add_patch(loom)


def create_loom_patch(
    start,
    upsample_factor=1,
    vertical=True,
    height=1.3,
    loom_n_samples=14,
    y=-0.2,
):
    width = loom_n_samples * upsample_factor
    x = start * upsample_factor
    if not vertical:
        width, height = height, width
        x, y = y, x
    return patches.Rectangle(
        (x, y),
        width,
        height,
        alpha=0.1,
        color="k",
        linewidth=0,
    )


def plot_line_with_color_variable(
    x, y, color_variable_array, start=None, normalising_factor=None
):

    """
    modified from: https://stackoverflow.com/questions/10252412/matplotlib-varying-color-of-line-to-capture-natural-time-parameterization-in-da

    meant for plotting speeds on tracks

    :param start:
    :param normalising_factor:
    :param x:
    :param y:
    :param color_variable_array:
    :return:
    """

    points = np.array([x, y]).transpose().reshape(-1, 1, 2)
    color_variable_array = np.array(
        [
            val
            for (p, val) in zip(points, color_variable_array)
            if not np.isnan(p).any()
        ]
    )
    points = np.array([p for p in points if not np.isnan(p).any()])

    if start is None:
        norm_factor = 1
    else:
        norm_factor = max(color_variable_array)
        points = points[start:]
        color_variable_array = color_variable_array[start:]

    points = np.array(
        [
            p
            for (p, val) in zip(points, color_variable_array)
            if not np.isnan(val)
        ]
    )
    color_variable_array = np.array(
        [val for val in color_variable_array if not np.isnan(val)]
    )

    if normalising_factor is not None:
        norm_factor = normalising_factor

    color_variable_array /= norm_factor

    segs = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(
        segs,
        cmap=plt.get_cmap("inferno"),
        norm=matplotlib.colors.Normalize(vmin=0, vmax=0.8),
    )
    lc.set_array(color_variable_array)

    plt.gca().add_collection(lc)

    plt.plot(color_variable_array)


def plot_trials_separate_plots(trials):
    fig, axes = plt.subplots(len(trials))
    for t, ax in zip(trials, axes):
        plt.axes(ax)
        t.plot_track()


def format_plots(axes):
    plt.subplots_adjust(wspace=1, hspace=1)
    for i, ax in enumerate(axes):
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)


def format_ax(xlabel="contrast", ylabel="escape probability", ax=None):
    if ax is None:
        ax = plt.gca()

    plt.ylabel(ylabel, fontsize=15, fontweight="black", color="#333F4B")
    plt.xlabel(xlabel, fontsize=15, fontweight="black", color="#333F4B")

    ax.spines["left"].set_smart_bounds(True)
    ax.spines["bottom"].set_smart_bounds(True)

    # set the spines position
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position(("axes", -0.04))
    ax.spines["left"].set_position(("axes", 0.015))


def convert_x_axis(n_samples, n_steps, frame_rate):
    plt.xticks(
        np.linspace(0, n_samples - 1, n_steps),
        np.round(np.linspace(0, n_samples / frame_rate, n_steps),2),
    )


def convert_y_axis(old_min, old_max, new_min, new_max, n_steps):
    plt.yticks(
        np.linspace(old_min, old_max, n_steps),
        np.linspace(new_min, new_max, n_steps),
    )


def get_x_length(ax=None):
    if ax is None:
        ax = plt.gca()
    line = ax.lines[0]
    xdata = line.get_xdata()
    return len(xdata)


def neaten_plots(axes, top=True, right=True, left=False, bottom=False):
    for ax in axes:
        sns.despine(ax=ax, top=top, right=right, left=left, bottom=bottom)


def laser_control(mtg, start_trial=0):
    fig=plt.figure()
    plt.title(mtg.mouse_id)

    distance_laser_on = []
    distance_laser_off = []
    img = np.load("/ceph/margrie/juliaw/rawdata/optostim_experiments/background_frame.npy")
    plt.imshow(img)
    trials = mtg.loom_trials()[start_trial:]
    laser_trials = [t for t in trials if t.has_laser][:5]
    no_laser_trials = [t for t in trials if not t.has_laser][:5]

    for t in laser_trials+no_laser_trials:

        distance_analysis = t.track.distance_analysis()

        if distance_analysis is not None:
            baseline_track, stimulus_track, baseline_distance, stimulus_distance = distance_analysis
            c = 'b' if t.has_laser else 'k'
            cumulative_distance_baseline = np.sum(baseline_distance)
            cumulative_distance_stimulus = np.sum(stimulus_distance)

            print(f"DISTANCE_BASELINE: {cumulative_distance_baseline} vs DISTANCE_STIMULUS: {cumulative_distance_stimulus}")

            distance_laser_on.append(cumulative_distance_stimulus) if t.has_laser else distance_laser_off.append(cumulative_distance_stimulus)
            text = '{0:.5f}'.format(cumulative_distance_stimulus)
            plt.text(stimulus_track[0][0], stimulus_track[1][0], text, color=c)
            #plt.plot(baseline_track[0], baseline_track[1], color='k')
            plt.plot(stimulus_track[0], stimulus_track[1], color=c)
    fig.savefig(f"/ceph/margrie/juliaw/derivatives/figures/{mtg.mouse_id}_positive_control_example_image.svg", format='svg')

    return distance_laser_on, distance_laser_off
