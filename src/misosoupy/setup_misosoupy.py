# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 10:53:23 2023

@author: hhanse
"""

from __future__ import division

import os  # handy system and path functions
from importlib import resources
from pathlib import Path
from warnings import warn

import pkg_resources

import configparser


# Ensure that relative paths start from the same directory as this script
def get_home_dir():
    """
    Get the home directory.

    Return the path name of the home directory where the script is saved,
    and change to that directory (if not already there).
    """

    home_dir = os.path.dirname(os.path.abspath(__file__))
    # NOTE: needed to manually change directory to /src/misosoupy/,
    # since pwd and os.path were returning the directory above?
    os.chdir(home_dir)

    return home_dir


def get_participant_id():
    """Take user input of the participant ID (string) and return as variable "participant"."""

    print("Please enter Participant ID:")
    participant = input()
    if len(participant) < 1:  # if no input
        participant = "TEST"
    print("ID is:", participant)

    return participant


def get_sound_list():
    """Take user input of the desired sound list and return as variable "source_sound_list"."""

    print(
        'Choose your sound list: Press "1" for soundlist.csv (FOAMS), or "2" for naturalsounds165'
    )
    sound_list_choice = int(input())

    if sound_list_choice == 1:
        source_sound_list = "sound_list.csv"  # FOAMS
    elif sound_list_choice == 2:
        source_sound_list = "naturalsounds165"
    else:
        print("Cannot determine sound list choice!")

    print("Sound List is:", source_sound_list)

    return source_sound_list


def get_path_to_assets():
    """Get the path to the assets directory"""
    try:
        import misosoupy
    except ImportError:
        # Consider updating this warning if we put misosoupy on PyPI
        warn("Could not find 'misosoupy' package. Did you run 'pip install -e .'?")
        return Path(__file__).absolute().parent / "assets"
    if hasattr(resources, "files"):
        return Path(resources.files(misosoupy) / "assets")
    else:
        return Path(pkg_resources.resource_filename("misosoupy", "assets"))

# Read in config file
# (code from https://medium.com/@lelambonzo/simplifying-configuration-file-parsing-in-python-ef8e2144b3b3)
def parse_config_file(config_path): 
    config = configparser.ConfigParser()
    config.read(config_path)

    steps_to_complete = {}
    for key, value in config['STEPS'].items():
        if value.lower() in 'true':
            steps_to_complete[key] = True
        elif value.lower() in 'false':
            steps_to_complete[key] = False

    screen_parameters = {}
    for key, value in config['SCREEN'].items():
        if value.isdigit():
            screen_parameters[key] = int(value)
        elif value.lower() in 'true':
            screen_parameters[key] = True
        elif value.lower() in 'false':
            screen_parameters[key] = False
        else:    
            try:
                screen_parameters[key] = float(value) 
            except:
                screen_parameters[key] = value

    return steps_to_complete, screen_parameters