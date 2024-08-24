# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:53:23 2023

@author: hhanse
"""

from __future__ import division

import os  # handy system and path functions
from pathlib import Path

import numpy as np

"""
===============================================================================
                        DEFINE FUNCTIONS
===============================================================================
"""


def function_import_sound_list(home_dir, source):
    """Read desired sound list and parse for unique labels.

    Parameters
    ----------
    home_dir : str
        The parent directory in which the sound list or folder of sounds is saved.
        Assumed to be the same directory as where scripts are located. Defined in setup_misosoupy.py.
    source : str
        The name of the sound list file (e.g., sound_list.csv) or folder of sounds (e.g., naturalsounds165/).
        Defined in setup_misosoupy.py.

    Returns
    -------
    all_sound_files : numpy array
        A list of the sound file names, as listed in the file or folder.
        Length will equal total number of sounds.
            Examples:
                sound_list.csv: 30709, 84275, etc.
                naturalsounds165/: stim102_crumpling_paper.wav, stim103_crying.wav, etc.
    all_sound_labels : numpy array
        A list of the sound labels, as listed in the file or folder (parsed from file names).
        Length will equal total number of sounds.
            Examples:
                    sound_list.csv: 'human_breathing', 'plastic_crumpling', etc.
                    naturalsounds165/: 'crumpling_paper', 'crying', etc.
    unique_sound_labels : numpy array
        A list of unique sound labels (i.e., all_sound_labels but ignoring duplicates), in alphabetical order.
        Use for participant selection onscreen.

    Raises
    ------
    Exception
        If path to sound list file or folder cannot be found.
        Check directory structure, and ensure sound list is in current working directory.
    """

    print("\n>>>>>>>>>>> Importing Sound List .................................")

    full_source_path = Path(home_dir, source)
    # Parse sound list source
    if full_source_path.is_file():

        label_spreadsheet_file = full_source_path

        # Open sound spreadsheet
        text_array = np.array([])
        with open(label_spreadsheet_file, "r") as t:
            for line in t:
                line_clean = line[:-1]  # removes the new line characters from the end
                row = line_clean.split(
                    ","
                )  # convert to list instead of string with commas
                sound_ID = row[0]
                sound_label = row[1]
                if len(text_array) == 0:  # if first row, save as headers
                    text_array = np.array(row[0:])
                else:
                    text_array = np.vstack([text_array, [sound_ID, sound_label]])
                # Save variables
            text_array = text_array[1:, :]
            all_sound_files = text_array[:, 0]
            all_sound_labels = text_array[:, 1]

    elif full_source_path.is_dir():

        all_sound_files = np.array([])
        all_sound_labels = np.array([])

        for item in os.listdir(full_source_path):
            if not item.startswith("."):
                all_sound_files = np.append(all_sound_files, item)
                item_label_temp = item.partition("_")[
                    2
                ]  # returns string after first underscore
                item_label = item_label_temp.partition(".")[
                    0
                ]  # returns string before file extension
                all_sound_labels = np.append(all_sound_labels, item_label)

    else:
        raise Exception(
            "Can't parse sound list! Path of sound list not found: "
            + str(full_source_path)
        )

    # Count number of unique labels to present
    unique_sound_labels = np.unique(all_sound_labels)

    print("Number of Sounds: ", len(all_sound_files))
    print("Number of Labels: ", len(unique_sound_labels))
    print(
        "Labels: ",
        list(unique_sound_labels)[0:10],
        "...\n" if len(unique_sound_labels) > 10 else "\n",
    )

    return all_sound_files, all_sound_labels, unique_sound_labels
