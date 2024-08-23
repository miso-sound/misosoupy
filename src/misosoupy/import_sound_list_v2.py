# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:53:23 2023

@author: hhanse
"""

from __future__ import division

import math
import os  # handy system and path functions

import numpy as np


"""
===============================================================================
                        DEFINE FUNCTIONS
===============================================================================
"""

##############################################################################
def function_import_sound_list(home_dir,participant,source):
    # Example:
        # source = "sound_list.csv", "naturalsounds165"

    print('\n>>>>>>>>>>> Importing Sound List .................................')
    
    
    # Parse sound list source
    if os.path.isfile(source):
    
        label_spreadsheet_file = home_dir + os.sep + source

        # Open sound spreadsheet
        text_array = np.array([])
        with open(label_spreadsheet_file, "r") as t:
            for line in t:
                line_clean = line[:-1]  # removes the new line characters from the end
                row = line_clean.split(",")  # convert to list instead of string with commas
                sound_ID = row[0]
                sound_label = row[1]
                if len(text_array) == 0:  # if first row, save as headers
                    text_array = np.array(row[0:])
                else:
                    text_array = np.vstack(
                        [text_array, [sound_ID, sound_label]]
                    )
                # Save variables
            text_array = text_array[1:, :]
            all_sound_files = text_array[:, 0]
            all_sound_labels = text_array[:, 1]
            
    elif os.path.isdir(source):
        
        all_sound_files=np.array([])
        all_sound_labels=np.array([])
        
        for item in os.listdir(source):
            if not item.startswith('.'):
                all_sound_files=np.append(all_sound_files,item)
                item_label_temp=item.partition('_')[2] #returns string after first underscore
                item_label=item_label_temp.partition('.')[0] #returns string before file extension
                all_sound_labels=np.append(all_sound_labels,item_label)
        
    else:
        raise Exception("Can't parse sound list!")    

    
    # Count number of unique labels to present
    unique_sound_labels = np.unique(all_sound_labels)
    
    print('Number of Sounds: ', len(all_sound_files))
    print('Number of Labels: ', len(unique_sound_labels))
    print('Labels: ', list(unique_sound_labels)[0:10],'...\n' if len(unique_sound_labels)>10 else '\n') 
    
    return all_sound_files, all_sound_labels, unique_sound_labels

##############################################################################

