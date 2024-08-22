# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:53:23 2023

@author: hhanse
"""

from __future__ import division

import math
import os  # handy system and path functions

import numpy as np

def function_import_sound_list(categorySpreadsheetName,numColumnsPerPage,numItemsPerColumn):
    # Example:
        # categorySpreadsheetName = "AllSoundCategories_v2.csv"
        # numColumnsPerPage = 2 # How many columns will appear on the screen
        # numItemsPerColumn = 10 # How many words (rows) will appear in each column

    """
    -------------------------------------------------------------------------------
                            Set up paths
    -------------------------------------------------------------------------------
    """
    
    # Ensure that relative paths start from the same directory as this script
    homeDir = os.path.dirname(os.path.abspath("__file__"))
    os.chdir(homeDir)
    categorySpreadsheetFile = homeDir + os.sep + categorySpreadsheetName
    
    """
    -------------------------------------------------------------------------------
                            Read in sound list
    -------------------------------------------------------------------------------
    """
    # Open sound spreadsheet
    txtArray = np.array([])
    with open(categorySpreadsheetFile, "r") as t:
        for line in t:
            line_clean = line[:-1]  # removes the new line characters from the end
            row = line_clean.split(",")  # convert to list instead of string with commas
            soundCategory = row[1]
            soundLabel = row[2]
            soundSource = row[3]
            soundFile = row[4]
            if len(txtArray) == 0:  # if first row, save as headers
                txtArray = np.array(row[1:])
            else:
                txtArray = np.vstack(
                    [txtArray, [soundCategory, soundLabel, soundSource, soundFile]]
                )
    
    # Save variables
    txtArray = txtArray[1:, :]
    allSoundCategories = txtArray[:, 0]
    allSoundLabels = txtArray[:, 1]
    allSoundSources = txtArray[:, 2]
    allSoundFiles = txtArray[:, 3]
    
    # Count number of unique labels to present
    uniqueSoundLabels = np.unique(allSoundLabels)
    numSoundLabels = len(uniqueSoundLabels)
    numItemsPerPage = numItemsPerColumn * numColumnsPerPage
    numPages = math.ceil(numSoundLabels / numItemsPerPage)  # round up if not even
    
    return allSoundCategories, allSoundLabels, allSoundSources, allSoundFiles, uniqueSoundLabels, numItemsPerColumn, numItemsPerPage, numPages
