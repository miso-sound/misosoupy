# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 10:53:23 2023

@author: hhanse
"""

from __future__ import division

import os  # handy system and path functions

# Ensure that relative paths start from the same directory as this script
def get_home_dir():
    home_dir = os.path.dirname(os.path.abspath("__file__")) #NOTE: needed to manually change directory to /src/misosoupy/, since pwd and os.path were returning the directory above?
    os.chdir(home_dir)

    return home_dir


def get_participant_id():
    print('Please enter Participant ID:')
    participant=input()
    if len(participant) < 1: #if no input
        participant='TEST'
    print('ID is:',participant)

    return participant


def get_sound_list():
    print('Choose your sound list: Press "1" for soundlist.csv (FOAMS), or "2" for naturalsounds165')
    sound_list_choice=int(input())

    if sound_list_choice == 1:
        source_sound_list='sound_list.csv' #FOAMS
    elif sound_list_choice == 2:
        source_sound_list='naturalsounds165'
    else:
        print('Cannot determine sound list choice!')

    print('Sound List is:',source_sound_list)

    return source_sound_list
