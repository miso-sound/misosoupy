# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:16:40 2024

@author: heath
"""
from __future__ import division

import time


# --- Import packages ---
from psychopy import core, event, visual, logging

def exitOut(win):
       logging.flush()
       win.close()
       core.quit()
       
def presentItemList(uniqueSoundLabels, 
                    numColumnsPerPage, 
                    numItemsPerColumn, 
                    numItemsPerPage, 
                    meanLength, 
                    itemHeight, 
                    squareOutlineSize, 
                    squareSize,
                    textColor, 
                    screenColor,
                    continueShapeColor,
                    shapeLineColor, 
                    win, 
                    pageNum, 
                    pauseTime, 
                    instr1, 
                    instr2, 
                    instr2color, 
                    instr3, 
                    initSquares, 
                    mostTriggeringList, 
                    doneWithMostTriggering):
    xPosCenter = (
        2 / numColumnsPerPage
    ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
    yPosCenter = (
        (numItemsPerColumn * itemHeight) / 2
    ) + itemHeight * 4.5  # items*height gives total screen needed, /2 to split equally b/w top and bottom half of screen

    allWordPosValues = []
    allSquarePosValues = []
    for iXpos in range(numColumnsPerPage):
        currXpos = (
           xPosCenter + 0.1 + 0.65 * (iXpos) # xPosCenter + 0.1 + 0.6 * (iXpos)
        )  # first column starts at center, next shifts right
        for iYpos in range(numItemsPerColumn):
            currYpos = (
                yPosCenter
                - (squareOutlineSize / 2)
                - squareOutlineSize * 1.25 * (iYpos)
            )

            # allWordPosValues.append((currXpos + 0.35, currYpos))  # [iYpos]))
            # allSquarePosValues.append((currXpos - 0.2, currYpos))
            allWordPosValues.append((currXpos + 0.3, currYpos))  # [iYpos]))
            allSquarePosValues.append((currXpos - 0.25, currYpos))

    currPageItems = uniqueSoundLabels[
        0 + pageNum * numItemsPerPage : numItemsPerPage + pageNum * numItemsPerPage
    ]
    allScreenWords = []
    allBoxes = []
    for iItem in range(0, len(currPageItems)):
        if len(currPageItems[iItem]) > meanLength: #16 # for long labels, decrease font size
            currItemHeight=itemHeight-0.005
        else:
            currItemHeight=itemHeight
        if len(currPageItems[iItem]) > meanLength*2: # for really long labels, put on two lines
            currItemHeight=currItemHeight-0.005
            currItemText_temp=currPageItems[iItem].replace("_", " ")
            currSpaceIdx=[i for i in range(len(currItemText_temp)) if currItemText_temp.startswith(" ",i)]
            if len(currSpaceIdx) > 4:
                currItemBreakPoint=currSpaceIdx[3] #break on 4th space
            else:
                currItemBreakPoint=currSpaceIdx[-1] #break on last space
            currItemText=currItemText_temp[:currItemBreakPoint] + '\n\t' + currItemText_temp[currItemBreakPoint:]
        else:
            currItemText=currPageItems[iItem].replace("_", " ")
        if doneWithMostTriggering:
            if (
                currPageItems[iItem] in mostTriggeringList
            ):  # make sounds already chosen unclickable
                allScreenWords.append(
                    visual.TextStim(
                        win,
                        text=currItemText,
                        pos=allWordPosValues[iItem],
                        color="gray",
                        height=currItemHeight,
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
                        text=currItemText,
                        pos=allWordPosValues[iItem],
                        color=textColor,
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
        else:
            allScreenWords.append(
                visual.TextStim(
                    win,
                    text=currItemText,
                    pos=allWordPosValues[iItem],
                    color=textColor,
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
        text="CONTINUE", #"Click here to continue",
        pos=(0.7, -0.85),
        color=screenColor,
        height=0.08,
    )
    backText = continueText
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
        text="EXIT", #"Click here to continue",
        pos=(.75, 0.9),
        color=textColor,
        height=0.08,
    )
    continueShape = exitShape
    backShape = exitShape
    
    # If page has been completed, re-present choices
    if len(initSquares) > 0:
        for i in range(len(initSquares)):
            if initSquares[i]==1:
                allBoxes[i]=visual.ShapeStim(win, vertices=((-.5, -.3), (-.5, .3), (.5, .3), (.5, -.3)), pos=allSquarePosValues[i], size=(squareSize*.5,squareSize*1.5), opacity=100, fillColor=shapeLineColor, lineColor=shapeLineColor,lineWidth=3.0)
        itemsChosen = initSquares
    else:
        itemsChosen = [0 for i in range(len(currPageItems))]

    Mouse = event.Mouse(win=win, visible=True)
    Mouse.clickReset()
    event.clearEvents()
    previousMouseDown = False

    itemClicked = False
    continueChosen = False
    backChosen = False
    # itemsChosen = [0 for i in range(len(currPageItems))]
    startTime = time.time()
    while continueChosen is False and backChosen == False:
        for i in allScreenWords:
            i.draw()
        for j in allBoxes:
            j.draw()
        instructTxt1.draw()
        instructTxt2.draw()
        instructTxt3.draw()
        backShape.draw()
        backText.draw()
        continueShape.draw()
        continueText.draw()
        exitShape.draw()
        exitText.draw()
        win.flip()

        if Mouse.isPressedIn(exitShape):
            exitOut(win)   

        # Check for checkbox clicks
        for s in range(0, len(allBoxes)):
            if Mouse.isPressedIn(allBoxes[s]):
                mouseDown = Mouse.getPressed()[0]
                if (
                    mouseDown and not previousMouseDown
                ):  # Only add to list if new click (otherwise, outputs each time frame refreshes, even if in the same button click)
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
                text="CONTINUE", #"Click here to continue",
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
            exitText.draw()
            win.flip()
            
        if pageNum != 0: #after first page, give option to go back to previous
            backText = visual.TextStim(win, text='BACK', pos=(xPosCenter-.05, -.85), color='white', height=0.08) 
            backShape = visual.ShapeStim(win, vertices=((-.5, -.3), (-.5, .3), (.5, .3), (.5, -.3)), pos=(xPosCenter-.05, -.85), size=(.25, .2), opacity=100, fillColor='black', lineColor=shapeLineColor,lineWidth=4.0,name='continueShape')
        
            if Mouse.isPressedIn(backShape):
                for i in allScreenWords:
                    i.draw()
                for j in allBoxes:
                    j.draw()
                instructTxt1.draw()
                instructTxt2.draw()
                instructTxt3.draw()    
                backChosen = True
                continueShape.draw()
                continueText.draw()
                exitShape.draw()
                exitText.draw()
                win.flip()     

    return itemsChosen, backChosen  # results are a list of 0s and 1s
