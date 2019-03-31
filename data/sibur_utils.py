"""Convenient routines for Sibur Challenge."""

from __future__ import print_function

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def visualize(data_stream, runs, coke_windows, title,
              each=10, alpha=0.3, run_color="forestgreen",
              coke_color="royalblue", figsize=(12,4)):
    """
    Visualize stream with overlay of run windows and coke windows."""

    plt.figure(figsize=figsize)

    # Plot data stream
    data_stream.iloc[::each].plot(linewidth=1, ax=plt.gca())

    ax = plt.gca()

    # Add overlays for runs
    for wi, window in runs.iterrows():
        ax.axvspan(window["run_start"], window["run_end"], alpha=alpha, color=run_color)

    # Add overlays for coke windows
    for wi, window in coke_windows.iterrows():
        ax.axvspan(window["start"], window["end"], alpha=alpha, color=coke_color)

    plt.title(title, fontsize=12)
    plt.tight_layout()
    plt.show()

def filter_overlaps(windows, distance):
    """Remove overlapping windows."""

    windows_srt = windows.sort_values(by="start")
    selected_windows = [windows_srt.iloc[0]]

    while True:
        ref_start = selected_windows[-1]["start"]
        candidates = windows_srt[windows_srt["start"]>(ref_start+distance)]

        if candidates.shape[0]==0:
            break
        selected_windows.append(candidates.iloc[0])

    return pd.concat(selected_windows, ignore_index=True, axis=1).T

def select_windows(start, stop, num_windows,
                   window_width=1, window_units="D",
                   sampling=1, sampling_units="T",
                   no_overlaps=True, verbose=True):
    """
    Select `num_windows` between `start` and `stop`, optionally excluding
    overlapping windows.
    """

    # Create all sample candidates
    dt_range = pd.date_range(start, stop-pd.Timedelta(window_width),
                             freq="%i%s" % (sampling, sampling_units))

    # Sample candidate windows
    selected_windows = np.random.choice(dt_range, num_windows, replace=False)
    selected_windows = pd.DataFrame(selected_windows, columns=["start"])

    # Calculate window end
    end_delta = (pd.Timedelta(window_width, unit=window_units)
                 - pd.Timedelta(sampling,
                                unit="m" if sampling_units=="T" else sampling_units))
    selected_windows["end"] = (selected_windows["start"] + end_delta)

    # Filter overlaps
    if not no_overlaps:
        return selected_windows
    else:
        selected_windows = filter_overlaps(selected_windows,
                                           pd.Timedelta(window_width,
                                                        unit=window_units))

        while selected_windows.shape[0]<num_windows:
            if verbose:
                print("Got %i windows..." % selected_windows.shape[0])

            selected_windows = pd.concat([selected_windows,
                                          select_windows(start, stop, num_windows,
                                                         window_width, window_units,
                                                         sampling, sampling_units,
                                                         no_overlaps=False)],
                                         ignore_index=True)
            selected_windows = filter_overlaps(selected_windows,
                                               pd.Timedelta(window_width,
                                                            unit=window_units))
    return selected_windows.iloc[:num_windows]
