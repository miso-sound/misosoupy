# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:38:17 2024

@author: heath
"""

from __future__ import division

import math

import numpy as np

# --- Import packages ---
from psychopy import core, event, logging, visual

def exitOut(win):
       logging.flush()
       win.close()
       core.quit()

def presentRefinedItemList(meanLength,
                           itemHeight,
                           squareOutlineSize, 
                           squareSize,
                           textColor,
                           screenColor, 
                           continueShapeColor,
                           shapeLineColor,
                           win,
                           items, 
                           pauseTime, 
                           instr1, 
                           instr2, 
                           instr2color):
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

            allWordPosValues.append((currXpos + (0.35), currYpos))  
            allSquarePosValues.append((currXpos - 0.2, currYpos))

    allScreenWords = []
    allBoxes = []
    allChoices = []
    for iItem in range(0, len(items)):
        if (
            numCols > 1 and len(items[iItem]) > meanLength 
        ):  # for long labels, decrease font size
            currItemHeight = refItemHeight - 0.005 #0.01
        else:
            currItemHeight = refItemHeight
        if len(items[iItem]) > meanLength*2: # for really long labels, put on two lines
            currItemHeight=currItemHeight-0.005
            currItemText_temp=items[iItem].replace("_", " ")
            currSpaceIdx=[i for i in range(len(currItemText_temp)) if currItemText_temp.startswith(" ",i)]
            if len(currSpaceIdx) > 4:
                currItemBreakPoint=currSpaceIdx[3] #break on 4th space
            else:
                currItemBreakPoint=currSpaceIdx[-1] #break on last space
            currItemText=currItemText_temp[:currItemBreakPoint] + '\n\t' + currItemText_temp[currItemBreakPoint:]
        else:
            currItemText=items[iItem].replace("_", " ")    
        allScreenWords.append(
            visual.TextStim(
                win,
                text=currItemText,
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
        text="CONTINUE", 
        pos=(0.7, -0.85),
        color=screenColor,
        height=0.08,
    )
    exitShape = visual.ShapeStim(
        win,
        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
        pos=(.75, 0.9),
        size=(0.35, 0.2),
        opacity=100,
        fillColor=screenColor,
        lineColor=shapeLineColor,
        lineWidth=4.0,
        name="exitShape",
    )
    exitText = visual.TextStim(
        win,
        text="EXIT", 
        pos=(.75, 0.9),
        color=textColor,
        height=0.08,
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
        exitText.draw()
        win.flip()

        if Mouse.isPressedIn(exitShape):
            win.close()
            core.quit()

        # Check for checkbox clicks
        for s in range(0, len(allBoxes)):
            if Mouse.isPressedIn(allBoxes[s]):
                mouseDown = Mouse.getPressed()[0]
                if (
                    mouseDown and not previousMouseDown
                ):  # Only add to list if new click (otherwise, outputs each time frame refreshes, even if in the same button click)
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
                text="CONTINUE", 
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
            exitText.draw()
            win.flip()

    allRanks = np.zeros(len(allChoices))
    for i in range(len(allChoices)):
        currItemRank = allChoices[i].text
        if currItemRank != " ":
            allRanks[i] = int(currItemRank)

    return itemsChosen, allRanks  # results are a list of 0s and 1s
