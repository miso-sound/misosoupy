# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:53:23 2023

@author: hhanse
"""

from __future__ import division

import math
import os  # handy system and path functions
import time

import numpy as np

# --- Import packages ---
from psychopy import core, data, event, gui, logging, visual

"""
###############################################################################
-------------------------------------------------------------------------------
                            SET UP EXPERIMENT
-------------------------------------------------------------------------------
###############################################################################
"""

fullScreenChoice = False  # make True during actual task
screenChoice = 0  # 2 #make 1 when only 1 monitor
screenSize = [1920, 1080]  # make [2048, 1152]
screenColor = "lightgray"
textColor = "black"
continueShapeColor = "gray"
shapeLineColor = "black"
itemHeight = 0.085
squareOutlineSize = 0.12
squareSize = 0.1
numColumnsPerPage = 2
numItemsPerColumn = 10
pauseTime = 2  # stay on item screen for 2s before skipping
categorySpreadsheetName = "AllSoundCategories_v2.csv"

psychopyVersion = "2022.2.5"
expName = "MISO_behav"  # from the Builder filename that created this script
exp_start_time = time.time()


# Ensure that relative paths start from the same directory as this script
homeDir = os.path.dirname(os.path.abspath("__file__"))
os.chdir(homeDir)
categorySpreadsheetFile = homeDir + os.sep + categorySpreadsheetName

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
            )  # line_clean)

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

"""
-------------------------------------------------------------------------------
                        Set up participant info
-------------------------------------------------------------------------------
"""


# this function controls the start of the experiment and pops up a box for the experimenter to enter participant number and condition
def ExpParameters():
    # Ensure that relative paths start from the same directory as this script
    expInfo = {
        "participant": "",
    }
    # --- Show participant info dialog --
    dlgBox = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlgBox.OK == False:
        core.quit()  # user pressed cancel
    expInfo["date"] = data.getDateStr()  # add a simple timestamp
    expInfo["expName"] = expName
    expInfo["psychopyVersion"] = psychopyVersion

    # Where data will save
    dataDir = homeDir + os.sep + "data" + os.sep  # + expInfo['participant']
    if not os.path.isdir(dataDir):
        os.mkdir(dataDir)

    return expInfo, dataDir  # outputFilename


# Show dialog box, save output variables to use elsewhere
expInfo, dataDir = ExpParameters()


# %%
"""
-------------------------------------------------------------------------------
                        DEFINE EXPERIMENT EXIT
-------------------------------------------------------------------------------

"""


def exitOut():
    logging.flush()
    win.close()
    core.quit()


# %%
"""
-------------------------------------------------------------------------------
                        Define functions
-------------------------------------------------------------------------------

"""


def presentInstructions(instructionText, waitTime):
    # Prep instructions
    instructTxt1 = visual.TextStim(
        win, text=instructionText, pos=(0, 0), color=textColor, height=0.09, wrapWidth=6
    )  # height=0.12, alignText='Left')
    # # Prep Continue Button
    # continueShape = visual.ShapeStim(win, vertices=((-.7, -.3), (-.7, .3), (.7, .3), (.7, -.3)), pos=(0, -.75), size=(1.5, .05), opacity=100, fillColor=continueShapeColor, lineColor=shapeLineColor,lineWidth=4.0)
    continueText = visual.TextStim(
        win,
        text="Click here to continue",
        pos=(0.7, -0.85),
        color=screenColor,
        height=0.08,
    )
    exitShape = visual.ShapeStim(
        win,
        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
        pos=(1, 1),
        size=(0.35, 0.35),
        opacity=100,
        fillColor=screenColor,
        lineColor=None,
        lineWidth=4.0,
        name="exitShape",
    )
    continueShape = exitShape

    Mouse = event.Mouse(win=win, visible=True)
    Mouse.clickReset()
    event.clearEvents()

    continueChosen = False
    instructTxt1.draw()
    continueShape.draw()
    continueText.draw()
    exitShape.draw()
    win.flip()
    core.wait(waitTime)
    while continueChosen == False:
        instructTxt1.draw()
        continueShape.draw()
        continueText.draw()
        exitShape.draw()
        win.flip()

        if Mouse.isPressedIn(exitShape):
            win.close()
            core.quit()

        # Make Continue Button visible after 3 seconds
        continueShape = visual.ShapeStim(
            win,
            vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
            pos=(0.7, -0.85),
            size=(0.45, 0.2),
            opacity=100,
            fillColor=continueShapeColor,
            lineColor=shapeLineColor,
            lineWidth=4.0,
            name="continueShape",
        )
        continueText = visual.TextStim(
            win,
            text="Click here to continue",
            pos=(0.7, -0.85),
            color=textColor,
            height=0.08,
        )

        if Mouse.isPressedIn(continueShape):
            instructTxt1.draw()
            continueShape.draw()
            continueText.draw()
            win.flip()
            continueChosen = True


# %%
def presentItemList(pageNum, pauseTime, instr1, instr2, instr2color, instr3):
    xPosCenter = (
        2 / numColumnsPerPage
    ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
    yPosCenter = (
        (numItemsPerColumn * itemHeight) / 2
    ) + itemHeight * 4  # items*height gives total screen needed, /2 to split equally b/w top and bottom half of screen

    allWordPosValues = []
    allSquarePosValues = []
    for iXpos in range(numColumnsPerPage):
        currXpos = (
            xPosCenter + 0.1 + 0.6 * (iXpos)
        )  # first column starts at center, next shifts right
        for iYpos in range(numItemsPerColumn):
            currYpos = (
                yPosCenter
                - (squareOutlineSize / 2)
                - squareOutlineSize * 1.25 * (iYpos)
            )

            allWordPosValues.append((currXpos + 0.35, currYpos))  # [iYpos]))
            allSquarePosValues.append((currXpos - 0.2, currYpos))

    currPageItems = uniqueSoundLabels[
        0 + iPage * numItemsPerPage : numItemsPerPage + iPage * numItemsPerPage
    ]
    allScreenWords = []
    allBoxes = []
    for iItem in range(
        0, len(currPageItems)
    ):  # (totalPicCount,totalPicCount+(numPicRows*numPicsPerRow)): #len(allDistTrialStim)):
        if doneWithMostTriggering:
            if (
                currPageItems[iItem] in mostTriggeringList
            ):  # make sounds already chosen unclickable
                allScreenWords.append(
                    visual.TextStim(
                        win,
                        text=currPageItems[iItem].replace("_", " "),
                        pos=allWordPosValues[iItem],
                        color="gray",
                        height=itemHeight,
                        alignText="Left",
                    )
                )
                allBoxes.append(
                    visual.ShapeStim(
                        win,
                        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                        pos=allSquarePosValues[iItem],
                        size=(0, 0),
                        opacity=100,
                        fillColor=None,
                        lineColor=shapeLineColor,
                        lineWidth=3.0,
                    )
                )
            else:
                allScreenWords.append(
                    visual.TextStim(
                        win,
                        text=currPageItems[iItem].replace("_", " "),
                        pos=allWordPosValues[iItem],
                        color=textColor,
                        height=itemHeight,
                        alignText="Left",
                    )
                )
                allBoxes.append(
                    visual.ShapeStim(
                        win,
                        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                        pos=allSquarePosValues[iItem],
                        size=(squareSize * 0.5, squareSize * 1.5),
                        opacity=100,
                        fillColor=None,
                        lineColor=shapeLineColor,
                        lineWidth=3.0,
                    )
                )
        else:
            allScreenWords.append(
                visual.TextStim(
                    win,
                    text=currPageItems[iItem].replace("_", " "),
                    pos=allWordPosValues[iItem],
                    color=textColor,
                    height=itemHeight,
                    alignText="Left",
                )
            )
            allBoxes.append(
                visual.ShapeStim(
                    win,
                    vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                    pos=allSquarePosValues[iItem],
                    size=(squareSize * 0.5, squareSize * 1.5),
                    opacity=100,
                    fillColor=None,
                    lineColor=shapeLineColor,
                    lineWidth=3.0,
                )
            )

    # # Prep Continue Button
    instructTxt1 = visual.TextStim(
        win, text=instr1, pos=(-0.7, 0.1), color=textColor, height=0.09, wrapWidth=6
    )  # height=0.12, alignText='Left')
    instructTxt2 = visual.TextStim(
        win, text=instr2, pos=(-0.7, 0.05), color=instr2color, height=0.09, wrapWidth=6
    )  # height=0.12, alignText='Left')
    instructTxt3 = visual.TextStim(
        win, text=instr3, pos=(-0.7, -0.85), color=textColor, height=0.09, wrapWidth=6
    )  # height=0.12, alignText='Left')
    continueText = visual.TextStim(
        win,
        text="Click here to continue",
        pos=(0.7, -0.85),
        color=screenColor,
        height=0.08,
    )
    exitShape = visual.ShapeStim(
        win,
        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
        pos=(1, 1),
        size=(0.35, 0.35),
        opacity=100,
        fillColor=screenColor,
        lineColor=None,
        lineWidth=4.0,
        name="exitShape",
    )
    continueShape = exitShape

    Mouse = event.Mouse(win=win, visible=True)
    Mouse.clickReset()
    event.clearEvents()
    previousMouseDown = False

    itemClicked = False
    continueChosen = False
    itemsChosen = [0 for i in range(len(currPageItems))]
    startTime = time.time()
    while continueChosen == False:
        for i in allScreenWords:
            i.draw()
        for j in allBoxes:
            j.draw()
        instructTxt1.draw()
        instructTxt2.draw()
        instructTxt3.draw()
        continueShape.draw()
        continueText.draw()
        exitShape.draw()
        win.flip()
        # core.wait(.5) #reset button press

        if Mouse.isPressedIn(exitShape):
            win.close()
            core.quit()

        # Check for checkbox clicks
        for s in range(0, len(allBoxes)):
            if Mouse.isPressedIn(
                allBoxes[s]
            ):  # button1shp.contains(Mouse): #Mouse.isPressedIn(button1shp):
                mouseDown = Mouse.getPressed()[0]
                if (
                    mouseDown and not previousMouseDown
                ):  # Only add to list if new click (otherwise, outputs each time frame refreshes, even if in the same button click)
                    if itemsChosen[s] == 0:  # item hasn't been chosen yet
                        if itemClicked == False:
                            itemClicked = True
                        itemsChosen[s] = 1
                        allBoxes[s] = visual.ShapeStim(
                            win,
                            vertices=(
                                (-0.5, -0.3),
                                (-0.5, 0.3),
                                (0.5, 0.3),
                                (0.5, -0.3),
                            ),
                            pos=allSquarePosValues[s],
                            size=(squareSize * 0.5, squareSize * 1.5),
                            opacity=100,
                            fillColor=shapeLineColor,
                            lineColor=shapeLineColor,
                            lineWidth=3.0,
                        )
                        core.wait(0.01)  # reset button press
                    elif (
                        itemsChosen[s] == 1
                    ):  # item was already chosen and is being de-selected
                        itemsChosen[s] = 0
                        allBoxes[s] = visual.ShapeStim(
                            win,
                            vertices=(
                                (-0.5, -0.3),
                                (-0.5, 0.3),
                                (0.5, 0.3),
                                (0.5, -0.3),
                            ),
                            pos=allSquarePosValues[s],
                            size=(squareSize * 0.5, squareSize * 1.5),
                            opacity=100,
                            fillColor=None,
                            lineColor=shapeLineColor,
                            lineWidth=3.0,
                        )
                    previousMouseDown = mouseDown
                    Mouse.clickReset()
                    event.clearEvents()
                    core.wait(0.25)
                    previousMouseDown = False

        # Make Continue Button visible after 1s
        currTime = time.time()
        if currTime - startTime > pauseTime:
            # if itemClicked == True:
            continueShape = visual.ShapeStim(
                win,
                vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                pos=(0.7, -0.85),
                size=(0.45, 0.2),
                opacity=100,
                fillColor=continueShapeColor,
                lineColor=shapeLineColor,
                lineWidth=4.0,
                name="continueShape",
            )
            continueText = visual.TextStim(
                win,
                text="Click here to continue",
                pos=(0.7, -0.85),
                color=textColor,
                height=0.08,
            )

        if Mouse.isPressedIn(continueShape):
            for i in allScreenWords:
                i.draw()
            for j in allBoxes:
                j.draw()
            instructTxt1.draw()
            instructTxt2.draw()
            instructTxt3.draw()
            continueChosen = True
            continueShape.draw()
            continueText.draw()
            exitShape.draw()
            win.flip()

    return itemsChosen  # results are a list of 0s and 1s


def presentRefinedItemList(items, pauseTime, instr1, instr2, instr2color):
    # Determine how many rows/columns are needed
    numItems = len(items)
    if numItems <= 12:
        numCols = 1
        numRows = numItems
        refItemHeight = itemHeight
        xPosCenter = 0  #
        colGap = 0.6
    elif numItems > 12 and numItems <= 24:
        numCols = 2
        numRows = math.ceil(numItems / 2)
        xPosCenter = (
            2 / numCols
        ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
        refItemHeight = itemHeight
        colGap = 0.6
    elif numItems > 24 and numItems <= 36:
        numCols = 3
        numRows = math.ceil(numItems / 3)
        refItemHeight = 0.075
        xPosCenter = (
            2 / numCols
        ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
        colGap = 0.45
    elif numItems > 36:
        numCols = 4
        numRows = math.ceil(numItems / 4)
        refItemHeight = 0.065
        xPosCenter = (
            2 / numCols
        ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
        colGap = 0.35

    yPosCenter = (
        (numRows * refItemHeight) / 2
    ) + refItemHeight * 5  # items*height gives total screen needed, /2 to split equally b/w top and bottom half of screen

    allWordPosValues = []
    allSquarePosValues = []
    for iXpos in range(numCols):
        currXpos = (
            xPosCenter + 0.1 + colGap * (iXpos)
        )  # first column starts at center, next shifts right
        for iYpos in range(numRows):
            currYpos = (
                yPosCenter
                - (squareOutlineSize / 2)
                - squareOutlineSize * 1.25 * (iYpos)
            )

            allWordPosValues.append((currXpos + (0.35), currYpos))  # [iYpos]))
            allSquarePosValues.append((currXpos - 0.2, currYpos))

    allScreenWords = []
    allBoxes = []
    allChoices = []
    for iItem in range(
        0, len(items)
    ):  # (totalPicCount,totalPicCount+(numPicRows*numPicsPerRow)): #len(allDistTrialStim)):
        if (
            numCols > 1 and len(items[iItem]) > 16
        ):  # for long labels, decrease font size
            currItemHeight = refItemHeight - 0.01
        else:
            currItemHeight = refItemHeight
        allScreenWords.append(
            visual.TextStim(
                win,
                text=items[iItem].replace("_", " "),
                pos=allWordPosValues[iItem],
                color=instr2color,
                height=currItemHeight,
                alignText="Left",
            )
        )
        allBoxes.append(
            visual.ShapeStim(
                win,
                vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                pos=allSquarePosValues[iItem],
                size=(squareSize * 0.5, squareSize * 1.5),
                opacity=100,
                fillColor=None,
                lineColor=shapeLineColor,
                lineWidth=3.0,
            )
        )
        allChoices.append(
            visual.TextStim(
                win, text=" ", color=textColor, height=refItemHeight, bold=True
            )
        )

    # # Prep Continue Button
    instructTxt1 = visual.TextStim(
        win, text=instr1, pos=(-0.7, 0.1), color=textColor, height=0.09, wrapWidth=6
    )  # height=0.12, alignText='Left')
    instructTxt2 = visual.TextStim(
        win, text=instr2, pos=(-0.7, 0.05), color=instr2color, height=0.09, wrapWidth=6
    )  # height=0.12, alignText='Left')
    continueText = visual.TextStim(
        win,
        text="Click here to continue",
        pos=(0.7, -0.85),
        color=screenColor,
        height=0.08,
    )
    exitShape = visual.ShapeStim(
        win,
        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
        pos=(1, 1),
        size=(0.35, 0.35),
        opacity=100,
        fillColor=screenColor,
        lineColor=None,
        lineWidth=4.0,
        name="exitShape",
    )
    resetShape = exitShape  # just temp placeholders
    resetText = continueText
    continueShape = exitShape

    Mouse = event.Mouse(win=win, visible=True)
    Mouse.clickReset()
    event.clearEvents()
    previousMouseDown = False

    # itemRanks = [1,2,3,4,5]
    allRanksChosen = False
    currRank = 1  # 0
    # itemClicked = False
    continueChosen = False
    # resetChosen = False
    itemsChosen = [0 for i in range(len(items))]
    # startTime = time.time()
    while continueChosen == False:
        for i in allScreenWords:
            i.draw()
        for j in allBoxes:
            j.draw()
        for c in allChoices:
            c.draw()
        instructTxt1.draw()
        instructTxt2.draw()
        # choiceTxt.draw()
        # instructTxt3.draw()
        continueShape.draw()
        continueText.draw()
        resetShape.draw()
        resetText.draw()
        exitShape.draw()
        win.flip()
        # core.wait(.5) #reset button press

        if Mouse.isPressedIn(exitShape):
            win.close()
            core.quit()

        # Check for checkbox clicks
        for s in range(0, len(allBoxes)):
            if Mouse.isPressedIn(
                allBoxes[s]
            ):  # button1shp.contains(Mouse): #Mouse.isPressedIn(button1shp):
                mouseDown = Mouse.getPressed()[0]
                if (
                    mouseDown and not previousMouseDown
                ):  # Only add to list if new click (otherwise, outputs each time frame refreshes, even if in the same button click)
                    if itemsChosen[s] == 0:  # item hasn't been chosen yet
                        # if itemClicked==False:
                        #     itemClicked=True
                        itemsChosen[s] = 1
                        allChoices[s].pos = allSquarePosValues[s]
                        allChoices[s].text = str(currRank)
                        # choiceTxt.pos=allSquarePosValues[s]
                        # choiceTxt.text=str(currRank)
                        # choiceTxt.setAutoDraw(True)
                        if currRank == 5:
                            allRanksChosen = True
                        else:
                            currRank += 1
                        # allBoxes[s]=visual.ShapeStim(win, vertices=((-.5, -.3), (-.5, .3), (.5, .3), (.5, -.3)), pos=allSquarePosValues[s], size=(squareSize*.5,squareSize*1.5), opacity=100, fillColor=shapeLineColor, lineColor=shapeLineColor,lineWidth=3.0)
                        core.wait(0.01)  # reset button press

                    elif (
                        itemsChosen[s] == 1
                    ):  # item was already chosen and is being de-selected
                        itemsChosen[s] = 0
                        # choiceTxt.pos=(0,0) #allSquarePosValues[s]
                        # choiceTxt.text=' '
                        allChoices[s].pos = (0, 0)
                        allChoices[s].text = " "
                        if currRank > 1:
                            currRank -= 1
                        # allBoxes[s]=visual.ShapeStim(win, vertices=((-.5, -.3), (-.5, .3), (.5, .3), (.5, -.3)), pos=allSquarePosValues[s], size=(squareSize*.5,squareSize*1.5), opacity=100, fillColor=None, lineColor=shapeLineColor,lineWidth=3.0)
                    previousMouseDown = mouseDown
                    Mouse.clickReset()
                    event.clearEvents()
                    core.wait(0.25)
                    previousMouseDown = False

        # Make Continue Button visible after 1s
        # currTime=time.time()

        if sum(itemsChosen) != 0:  # if they've clicked something, give option to reset
            resetText = visual.TextStim(
                win, text="RESET", pos=(-0.7, -0.85), color="white", height=0.08
            )
            resetShape = visual.ShapeStim(
                win,
                vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                pos=(-0.7, -0.85),
                size=(0.3, 0.2),
                opacity=100,
                fillColor="black",
                lineColor=shapeLineColor,
                lineWidth=4.0,
                name="continueShape",
            )

        if Mouse.isPressedIn(resetShape):
            # resetChosen = True
            itemsChosen = [0 for i in range(len(items))]
            currRank = 1
            continueShape = exitShape
            continueText = resetText
            for r in range(0, len(allBoxes)):
                allChoices[r].pos = (0, 0)
                allChoices[r].text = " "

        if allRanksChosen:  # currTime-startTime > pauseTime:
            # if itemClicked == True:
            continueShape = visual.ShapeStim(
                win,
                vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                pos=(0.7, -0.85),
                size=(0.45, 0.2),
                opacity=100,
                fillColor=continueShapeColor,
                lineColor=shapeLineColor,
                lineWidth=4.0,
                name="continueShape",
            )
            continueText = visual.TextStim(
                win,
                text="Click here to continue",
                pos=(0.7, -0.85),
                color=textColor,
                height=0.08,
            )

        if Mouse.isPressedIn(continueShape):
            for i in allScreenWords:
                i.draw()
            for j in allBoxes:
                j.draw()
            instructTxt1.draw()
            instructTxt2.draw()
            # instructTxt3.draw()
            continueChosen = True
            continueShape.draw()
            continueText.draw()
            exitShape.draw()
            win.flip()

    allRanks = np.zeros(len(allChoices))
    for i in range(len(allChoices)):
        currItemRank = allChoices[i].text
        if currItemRank != " ":
            allRanks[i] = int(currItemRank)

    return itemsChosen, allRanks  # results are a list of 0s and 1s


# %%
"""
###############################################################################
-------------------------------------------------------------------------------
                       SOUND SELECTIONS TASK
-------------------------------------------------------------------------------
###############################################################################

-------------------------------------------------------------------------------
                        SET UP WINDOW
-------------------------------------------------------------------------------

"""

# --- Setup the Window ---
win = visual.Window(
    size=screenSize,
    fullscr=fullScreenChoice,
    screen=screenChoice,
    color="lightgray",
    colorSpace="rgb",
    units="norm",
)
# winType='pyglet', allowStencil=False,
# monitor='testMonitor',
# blendMode='avg', useFBO=True)
# units='height')
# win.mouseVisible = False

instructions1 = (
    "In this experiment, you will listen to sounds."
    + "\nIt is important that we use the most effective sounds for each participant."
    + "\n\nOn the next pages, you will see the names of sounds. \nPlease select the sounds "
    + "that you find \nthe MOST triggering (e.g., bothersome, unpleasant) "
    + "and \nthe LEAST triggering (e.g., neutral, neither pleasant nor unpleasant)."
    + "\nDo this by clicking the box next to the sound name."
    + "\n\nThere will be 5 pages for each prompt (most and least). \nTry to choose AT LEAST 4-5 sounds for each prompt."
)
presentInstructions(instructions1, 1)


# %%
"""
-------------------------------------------------------------------------------
                        GET SOUND SELECTIONS
-------------------------------------------------------------------------------

----------------------  MOST triggering sounds

"""

instr1 = "First, please choose \nthe sounds you are \n\n triggered by.\n\n\nIf none of these sounds\nare triggering, \ncontinue to the \nnext page."
instr2 = "MOST\n\n\n\n\n\n"
# instr1='First, please choose \nthe sounds you find the \n\n\n\n\nIf none of these sounds\nare unpleasant, \ncontinue to the \nnext page.'
# instr2='MOST UNPLEASANT\n\n\n\n\n\n'

doneWithMostTriggering = False
mostTriggeringList = []
for iPage in range(numPages):
    instr3 = "Page " + str(iPage + 1) + "/" + str(numPages)
    mostTriggeringList_page = presentItemList(
        iPage, pauseTime, instr1, instr2, "red", instr3
    )
    for iItem in range(len(mostTriggeringList_page)):
        if mostTriggeringList_page[iItem] == 1:
            mostTriggeringList.append(
                uniqueSoundLabels[iItem + iPage * numItemsPerPage]
            )

doneWithMostTriggering = True
breakInstructions = "Great! \n\nOn the next page, you will see the sounds you selected. \n\nPlease choose your TOP 5 most triggering \nsounds from this list, and rank order them from \n1 (more triggering) to 5 (less triggering)."
presentInstructions(breakInstructions, 0)

instr1 = "Please rank the \n\nsounds you \nare triggered by. \n\n1 = more triggering\n5 = less triggering \n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page."
instr2 = "TOP 5\n\n\n\n\n\n\n\n\n\n"

refinedMostTriggeringList = []
# refinedTriggerIdx=np.zeros(len(mostTriggeringList))
[mostTriggeringList_refined, mostTriggering_ranks] = presentRefinedItemList(
    mostTriggeringList, pauseTime, instr1, instr2, "red"
)
for iItem in range(len(mostTriggeringList)):
    if mostTriggeringList_refined[iItem] == 1:
        refinedMostTriggeringList.append(
            [mostTriggering_ranks[iItem], mostTriggeringList[iItem]]
        )

refinedMostTriggeringList = sorted(refinedMostTriggeringList)


"""
---------------------- LEAST triggering sounds

"""
breakInstructions = "Next, you will repeat this process with sounds \nyou find the LEAST triggering or MOST NEUTRAL."
presentInstructions(breakInstructions, 0)

instr1 = "Now, please choose \nthe sounds you are \n\n triggered by.\n\n\nIf all of these sounds\nare triggering, \ncontinue to the \nnext page."
instr2 = "LEAST\n\n\n\n\n\n"
# instr1='Now, please choose \nthe sounds you find the \n\n\n\n\nIf all of these sounds\nare pleasant/unpleasant, \ncontinue to the \nnext page.'
# instr2='MOST NEUTRAL\n\n\n\n\n\n'

leastTriggeringList = []
for iPage in range(numPages):
    instr3 = "Page " + str(iPage + 1) + "/" + str(numPages)
    leastTriggeringList_page = presentItemList(
        iPage, pauseTime, instr1, instr2, "green", instr3
    )
    for iItem in range(len(leastTriggeringList_page)):
        if leastTriggeringList_page[iItem] == 1:
            leastTriggeringList.append(
                uniqueSoundLabels[iItem + iPage * numItemsPerPage]
            )

instr1 = "Please rank the \n\nsounds to you. \n\n1 = more neutral\n5 = less neutral \n\n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page."
instr2 = "5 MOST NEUTRAL\n\n\n\n\n\n\n\n\n\n"

refinedLeastTriggeringList = []
[leastTriggeringList_refined, leastTriggering_ranks] = presentRefinedItemList(
    leastTriggeringList, pauseTime, instr1, instr2, "green"
)
for iItem in range(len(leastTriggeringList)):
    if leastTriggeringList_refined[iItem] == 1:
        refinedLeastTriggeringList.append(
            [leastTriggering_ranks[iItem], leastTriggeringList[iItem]]
        )

refinedLeastTriggeringList = sorted(refinedLeastTriggeringList)

"""
-------------------------------------------------------------------------------
                            ORGANIZE SOUND SELECTIONS
-------------------------------------------------------------------------------

"""
# Show waiting screen
compileInstructions = "Please wait as we compile your chosen sounds...\n\nThe experiment will begin shortly!"
instructTxt1 = visual.TextStim(
    win, text=compileInstructions, pos=(0, 0), color=textColor, height=0.09, wrapWidth=6
)  # height=0.12, alignText='Left')
exitShape = visual.ShapeStim(
    win,
    vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
    pos=(1, 1),
    size=(0.35, 0.35),
    opacity=100,
    fillColor=screenColor,
    lineColor=None,
    lineWidth=4.0,
    name="exitShape",
)

Mouse = event.Mouse(win=win, visible=True)
Mouse.clickReset()
event.clearEvents()

soundsCompiled = False
instructTxt1.draw()
win.flip()
core.wait(2)
while soundsCompiled == False:
    instructTxt1.draw()
    exitShape.draw()
    win.flip()

    # Check for exit click
    if Mouse.isPressedIn(exitShape):
        win.close()
        core.quit()

    # Make output file to save selections
    # filename = homeDir + u'data\%s_%s_%s_%s' % (expInfo['participant'], expName,'SoundSelect',expInfo['date'] + '.txt')
    filename = dataDir + "\%s_%s_%s_%s" % (
        expInfo["participant"],
        expName,
        "SoundSelect",
        expInfo["date"] + ".txt",
    )
    with open(filename, "w") as textfile:
        print("SOUND_TYPE\t", "RANK\t", "SOUND_LABEL", file=textfile)

    # Cycle through selections to grab path names
    mostTriggerPaths = []
    mostTriggerCats = []
    rankPos = 0
    for iMost in mostTriggeringList:
        with open(filename, "a") as textfile:
            print(
                "Trigger\t\t",
                str(round(mostTriggering_ranks[rankPos])) + "\t",
                iMost,
                file=textfile,
            )
        # if round(mostTriggering_ranks[rankPos]) != 0:
        #     mostRows=txtArray[(allSoundLabels==iMost),:]
        #     for iRow in mostRows:
        #         if iRow[4] != '1': # Don't use standard sounds in personalized list
        #             currPath=homeDir+'\\allsounds\\BEHAV\\'+iRow[2]+'\\'+iRow[3]+'.wav'
        #             mostTriggerCats.append(iMost)
        #             mostTriggerPaths.append(currPath)
        rankPos += 1

    leastTriggerPaths = []
    leastTriggerCats = []
    rankPos = 0
    for iLeast in leastTriggeringList:
        with open(filename, "a") as textfile:
            print(
                "Neutral\t\t",
                str(round(leastTriggering_ranks[rankPos])) + "\t",
                iLeast,
                file=textfile,
            )
        # if round(leastTriggering_ranks[rankPos]) != 0:
        #     leastRows=txtArray[(allSoundLabels==iLeast),:]
        #     for iRow in leastRows:
        #         if iRow[4] != '1': # Don't use standard sounds in personalized list
        #             currPath=homeDir+'\\allsounds\\BEHAV\\'+iRow[2]+'\\'+iRow[3]+'.wav'
        #             leastTriggerCats.append(iLeast)
        #             leastTriggerPaths.append(currPath)
        rankPos += 1

    # Save paths to excel for use in behav script
    mostPaths = np.array([mostTriggerPaths]).T
    leastPaths = np.array([leastTriggerPaths]).T
    mostCats = np.array([mostTriggerCats]).T
    leastCats = np.array([leastTriggerCats]).T
    # standPaths=np.array([standardPaths]).T
    allPaths = np.vstack([mostPaths, leastPaths])  # ,standPaths])
    # df = DataFrame(allPaths.T,columns=['mysound'])
    # filepath_save=homeDir+'\\sounds\\sounds_behav_HHtest.xlsx'
    # df.to_excel(filepath_save,index=False)

    # # Make sure folders are empty, then copy files to correct folder
    # mostCopied=False
    # trigFolder=homeDir+'\\allsounds\\BEHAV\\PARTICIPANT_behav_trigger_HHtest\\'
    # if len(os.listdir(trigFolder)) > 1 and not mostCopied:
    #     for f in Path(trigFolder).glob("*"):
    #         if f.is_file():
    #             f.unlink()
    # for iMost in mostPaths:
    #     mostPath=iMost[0]
    #     mostName=mostPath.split('\\')[-1]
    #     destinationPath=trigFolder+mostName #+'.wav'
    #     shutil.copyfile(mostPath, destinationPath)
    # mostCopied=True

    # leastCopied=False
    # neutFolder=homeDir+'\\allsounds\\BEHAV\\PARTICIPANT_behav_neutral_HHtest\\'
    # if len(os.listdir(neutFolder)) > 1 and not leastCopied:
    #     for f in Path(neutFolder).glob("*"):
    #         if f.is_file():
    #             f.unlink()
    # for iLeast in leastPaths:
    #     leastPath=iLeast[0]
    #     leastName=leastPath.split('\\')[-1]
    #     destinationPath=neutFolder+leastName #+'.wav'
    #     shutil.copyfile(leastPath, destinationPath)
    # leastCopied=True

    # End waiting screen (Break while loop so files aren't added more than once)
    soundsCompiled = True


# file_mappings = []

# # Specify the source and destination folders
# source_folder5 = "allsounds/BEHAV/PARTICIPANT_behav_neutral_HHtest"
# destination_folder5 = "sounds/behav/soundneutralperso"

# for file_name in os.listdir(destination_folder5):
#     file_path = os.path.join(destination_folder5, file_name)
#     if os.path.isfile(file_path):
#         os.remove(file_path)

# # Iterate over the files in the source folder
# file_count = 0
# for filename in os.listdir(source_folder5):
#     if filename.endswith(".wav"):
#         file_count += 1
#         source_file = os.path.join(source_folder5, filename)
#         destination_file = os.path.join(destination_folder5, f"sound_neutral_perso_{file_count}.wav")
#         shutil.copyfile(source_file, destination_file)

#         filename_short=filename[:-4] #remove '.wav'
#         currCat=allSoundLabels[allSoundFiles==filename_short][0] #find corresponding label

#         file_mappings.append(('NEUTRAL',currCat,filename, f"sound_neutral_perso_{file_count}.wav"))


# print(f"Files successfully copied to {destination_folder5}!")

# # Specify the source and destination folders
# source_folder6 = "allsounds/BEHAV/PARTICIPANT_behav_trigger_HHtest"
# destination_folder6 = "sounds/behav/soundtriggerperso"

# for file_name in os.listdir(destination_folder6):
#     file_path = os.path.join(destination_folder6, file_name)
#     if os.path.isfile(file_path):
#         os.remove(file_path)

# # Iterate over the files in the source folder
# file_count = 0
# for filename in os.listdir(source_folder6):
#     if filename.endswith(".wav"):
#         file_count += 1
#         source_file = os.path.join(source_folder6, filename)
#         destination_file = os.path.join(destination_folder6, f"sound_trigger_perso_{file_count}.wav")
#         shutil.copyfile(source_file, destination_file)

#         filename_short=filename[:-4] #remove '.wav'
#         currCat=allSoundLabels[allSoundFiles==filename_short][0] #find corresponding label

#         file_mappings.append(('TRIGGER',currCat,filename, f"sound_trigger_perso_{file_count}.wav"))


# print(f"Files successfully copied to {destination_folder6}!")


# # Save reference excel files
# # filename2 = dataDir +u'\%s_%s_%s_%s' % (expInfo['participant'], expName,'SoundMappings',expInfo['date'] + '.xlsx')
# filename2 = dataDir +u'\%s_%s_%s_%s' % (expInfo['participant'], expName,'SoundMappings',expInfo['date'] + '.csv')
# df = DataFrame(file_mappings,columns=['SOUND_TYPE','SOUND_LABEL','SOUND_FILENAME','EXPERIMENT_LABEL'])
# # df.to_excel(filename2,index=False)
# df.to_csv(filename2,index=False)

# filename3 = homeDir+'\\sounds\\sounds_behav_HHtest.xlsx'

# allSoundPaths=[]
# for i in df.EXPERIMENT_LABEL:
#     if 'trigger_perso' in i:
#         subFolder='soundtriggerperso\\'
#     elif 'neutral_perso' in i:
#         subFolder='soundneutralperso\\'
#     allSoundPaths.append(homeDir+'\\sounds\\behav\\'+subFolder+i)
# # add standard sounds to file
# for i in range(5):
#     allSoundPaths.append(homeDir+'\\sounds\\behav\\soundtriggerstandard\\sound_trigger_stand_'+str(i+1)+'.wav')
# for i in range(5):
#     # allSoundPaths.append(homeDir+os.sep+'sounds'+os.sep+'behav'+os.sep+'neutralstandard'+os.sep+'neutral_stand_'+str(i+1)+'.wav')
#     allSoundPaths.append(homeDir+'\\sounds\\behav\\soundneutralstandard\\sound_neutral_stand_'+str(i+1)+'.wav')

# df2 = DataFrame(allSoundPaths,columns=['mysound'])
# df2.to_excel(filename3,index=False)

print("****************** READY TO START EXPERIMENT!")


# --- End experiment ---
instructions1 = (
    "Great!"
    + "\n\nYou have finished this session of tasks."
    + "\nPlease wait for your experimenter."
)
presentInstructions(instructions1, 2)
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

logging.flush()
# make sure everything is closed down


exitOut()
