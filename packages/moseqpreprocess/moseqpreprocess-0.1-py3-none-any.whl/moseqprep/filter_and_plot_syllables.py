from .plot_syl import plot_syllables


import numpy as np
import pandas as pd




def filter_and_plot_syllables(syllableraw_data:dict, index_diff, min_duration:int, max_duration:int, syllables=None):
    """
    Function to filter syllables based on duration and plot them.
    :param syllableraw_data: The raw syllable data.
    :param index_diff: The index_diff data containing durations.
    :param min_duration: Minimum duration for filtering.
    :param max_duration: Maximum duration for filtering.
    :param syllables: List of specific syllables to plot. If None, plot all syllables.
    """
    # Apply filtering directly on syllableraw_data based on index_diff

    for key, value in syllableraw_data.items():
        syllableraw_data[key] = value[
            (index_diff[key]['Duration'].astype('int') > min_duration) &
            (index_diff[key]['Duration'].astype('int') < max_duration)
            ]

    # If specific syllables are provided, filter the dictionary to keep only those syllables
    if syllables is not None:
        syllableraw_data = {key: syllableraw_data[key] for key in syllables if key in syllableraw_data}
        if len(syllableraw_data) == 0:
            print(f"None of the specified syllables {syllables} were found in the data.")
            return
    plot_syllables(syllableraw_data)




