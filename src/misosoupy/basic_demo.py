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

"""
-------------------------------------------------------------------------------
                        Set up participant info
-------------------------------------------------------------------------------
"""


# this function controls the start of the experiment and pops up a box for the
# experimenter to enter participant number and condition
def ExpParameters():
    # Ensure that relative paths start from the same directory as this script
    expInfo = {
        "participant": "",
    }
    # --- Show participant info dialog --
    dlgBox = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlgBox.OK is False:
        core.quit()  # user pressed cancel
    expInfo["date"] = data.getDateStr()  # add a simple timestamp
    expInfo["expName"] = expName
    expInfo["psychopyVersion"] = psychopyVersion

    # Where data will save
    dataDir = homeDir + os.sep + "data" + os.sep
    if not os.path.isdir(dataDir):
        os.mkdir(dataDir)

    return expInfo, dataDir


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
    )
    # Prep Continue Button
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
    while continueChosen is False:
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
    for iItem in range(0, len(currPageItems)):
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
    )
    instructTxt2 = visual.TextStim(
        win, text=instr2, pos=(-0.7, 0.05), color=instr2color, height=0.09, wrapWidth=6
    )
    instructTxt3 = visual.TextStim(
        win, text=instr3, pos=(-0.7, -0.85), color=textColor, height=0.09, wrapWidth=6
    )
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
    while continueChosen is False:
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

        if Mouse.isPressedIn(exitShape):
            win.close()
            core.quit()

        # Check for checkbox clicks
        for s in range(0, len(allBoxes)):
            if Mouse.isPressedIn(allBoxes[s]):
                mouseDown = Mouse.getPressed()[0]
                if mouseDown and not previousMouseDown:  # Only add to list if new click
                    # (otherwise, outputs each time frame refreshes, even if in the same button click)
                    if itemsChosen[s] == 0:  # item hasn't been chosen yet
                        if itemClicked is False:
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
    for iItem in range(0, len(items)):
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
    )
    instructTxt2 = visual.TextStim(
        win, text=instr2, pos=(-0.7, 0.05), color=instr2color, height=0.09, wrapWidth=6
    )
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

    allRanksChosen = False
    currRank = 1  # 0
    continueChosen = False
    itemsChosen = [0 for i in range(len(items))]
    while continueChosen is False:
        for i in allScreenWords:
            i.draw()
        for j in allBoxes:
            j.draw()
        for c in allChoices:
            c.draw()
        instructTxt1.draw()
        instructTxt2.draw()
        continueShape.draw()
        continueText.draw()
        resetShape.draw()
        resetText.draw()
        exitShape.draw()
        win.flip()

        if Mouse.isPressedIn(exitShape):
            win.close()
            core.quit()

        # Check for checkbox clicks
        for s in range(0, len(allBoxes)):
            if Mouse.isPressedIn(allBoxes[s]):
                mouseDown = Mouse.getPressed()[0]
                if mouseDown and not previousMouseDown:  # Only add to list if new click
                    # (otherwise, outputs each time frame refreshes, even if in the same button click)
                    if itemsChosen[s] == 0:  # item hasn't been chosen yet
                        itemsChosen[s] = 1
                        allChoices[s].pos = allSquarePosValues[s]
                        allChoices[s].text = str(currRank)
                        if currRank == 5:
                            allRanksChosen = True
                        else:
                            currRank += 1
                        core.wait(0.01)  # reset button press

                    elif (
                        itemsChosen[s] == 1
                    ):  # item was already chosen and is being de-selected
                        itemsChosen[s] = 0
                        allChoices[s].pos = (0, 0)
                        allChoices[s].text = " "
                        if currRank > 1:
                            currRank -= 1
                    previousMouseDown = mouseDown
                    Mouse.clickReset()
                    event.clearEvents()
                    core.wait(0.25)
                    previousMouseDown = False

        # Make Continue Button visible after 1s

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
            itemsChosen = [0 for i in range(len(items))]
            currRank = 1
            continueShape = exitShape
            continueText = resetText
            for r in range(0, len(allBoxes)):
                allChoices[r].pos = (0, 0)
                allChoices[r].text = " "

        if allRanksChosen:
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

instr1 = (
    "First, please choose \nthe sounds you are \n\n triggered by."
    + "\n\n\nIf none of these sounds\nare triggering, \ncontinue to the \nnext page."
)
instr2 = "MOST\n\n\n\n\n\n"

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
breakInstructions = (
    "Great! \n\nOn the next page, you will see the sounds you selected."
    + " \n\nPlease choose your TOP 5 most triggering \nsounds from this list, "
    + "and rank order them from \n1 (more triggering) to 5 (less triggering)."
)
presentInstructions(breakInstructions, 0)

instr1 = (
    "Please rank the \n\nsounds you \nare triggered by. "
    + "\n\n1 = more triggering\n5 = less triggering \n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page."
)
instr2 = "TOP 5\n\n\n\n\n\n\n\n\n\n"

refinedMostTriggeringList = []
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

instr1 = (
    "Now, please choose \nthe sounds you are \n\n triggered by.\n\n\nIf all of these sounds\nare triggering, "
    + "\ncontinue to the \nnext page."
)
instr2 = "LEAST\n\n\n\n\n\n"

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

instr1 = (
    "Please rank the \n\nsounds to you. "
    + "\n\n1 = more neutral\n5 = less neutral \n\n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page."
)
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

Mouse = event.Mouse(win=win, visible=True)
Mouse.clickReset()
event.clearEvents()

soundsCompiled = False
instructTxt1.draw()
win.flip()
core.wait(2)
while soundsCompiled is False:
    instructTxt1.draw()
    exitShape.draw()
    win.flip()

    # Check for exit click
    if Mouse.isPressedIn(exitShape):
        win.close()
        core.quit()

    # Make output file to save selections
    filename = dataDir + r"\%s_%s_%s_%s" % (
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
        rankPos += 1

    # Save paths to excel for use in behav script
    mostPaths = np.array([mostTriggerPaths]).T
    leastPaths = np.array([leastTriggerPaths]).T
    mostCats = np.array([mostTriggerCats]).T
    leastCats = np.array([leastTriggerCats]).T
    allPaths = np.vstack([mostPaths, leastPaths])
    soundsCompiled = True

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
