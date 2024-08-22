# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:53:23 2023

@author: hhanse
"""

from __future__ import division

import math
import os  # handy system and path functions

import numpy as np


# Ensure that relative paths start from the same directory as this script
homeDir = os.path.dirname(os.path.abspath("__file__"))
os.chdir(homeDir)
participant = 'TEST'

"""
===============================================================================
                        DEFINE FUNCTIONS
===============================================================================
"""

##############################################################################
def function_import_sound_list(source):
    # Example:
        # source = "sound_list.csv", "naturalsounds165"

    print('\n>>>>>>>>>>> Importing Sound List .................................')
    
    
    # Parse sound list source
    if os.path.isfile(source):
    
        labelSpreadsheetFile = homeDir + os.sep + source

        # Open sound spreadsheet
        txtArray = np.array([])
        with open(labelSpreadsheetFile, "r") as t:
            for line in t:
                line_clean = line[:-1]  # removes the new line characters from the end
                row = line_clean.split(",")  # convert to list instead of string with commas
                soundID = row[0]
                soundLabel = row[1]
                if len(txtArray) == 0:  # if first row, save as headers
                    txtArray = np.array(row[0:])
                else:
                    txtArray = np.vstack(
                        [txtArray, [soundID, soundLabel]]
                    )
                # Save variables
            txtArray = txtArray[1:, :]
            allSoundFiles = txtArray[:, 0]
            allSoundLabels = txtArray[:, 1]
            
    elif os.path.isdir(source):
        
        allSoundFiles=np.array([])
        allSoundLabels=np.array([])
        
        for item in os.listdir(source):
            if not item.startswith('.'):
                allSoundFiles=np.append(allSoundFiles,item)
                itemLabel_temp=item.partition('_')[2] #returns string after first underscore
                itemLabel=itemLabel_temp.partition('.')[0] #returns string before file extension
                allSoundLabels=np.append(allSoundLabels,itemLabel)
        
    else:
        raise Exception("Can't parse sound list!")    

    
    # Count number of unique labels to present
    uniqueSoundLabels = np.unique(allSoundLabels)
    
    print('Number of Sounds: ', len(allSoundFiles))
    print('Number of Labels: ', len(uniqueSoundLabels))
    print('Labels: ', list(uniqueSoundLabels)[0:10],'...\n' if len(uniqueSoundLabels)>10 else '\n') 
    
    return allSoundFiles, allSoundLabels, uniqueSoundLabels

##############################################################################

