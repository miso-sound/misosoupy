# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:02:55 2024

@author: heath

THINGS TO STILL ADD (JUN 8 2024):
    
    Option to set minimum required sounds (current default: 5 per category)
    Option to change instructions?
    Option to change colors
    Option to select sounds without needing psychopy?
    How to input preferences in run_misosoupy function, without needing to edit text
    Docstrings/comments


"""

from __future__ import division

import math
import os  # handy system and path functions

import numpy as np

# Set up preferences ################
step_importSoundList = True
step_selectSoundList = True
step_selectTrigger, step_selectNeutral = True, True
step_refineSoundList = True
step_refineTrigger, step_refineNeutral = True, True
step_organizeSounds = True

participant = 'TEST'
source_sound_list = "naturalsounds165" # "sound_list.csv" (FOAMS), "naturalsounds165"

# Ensure that relative paths start from the same directory as this script
homeDir = os.path.dirname(os.path.abspath("__file__"))
os.chdir(homeDir)

if step_importSoundList:
    import import_sound_list_v2
    [allSoundFiles, allSoundLabels, uniqueSoundLabels]=import_sound_list_v2.function_import_sound_list(source_sound_list) #'naturalsounds165' sound_list.csv
else:
    raise Exception("Need sounds to select from!")    
    
if step_selectSoundList or step_refineSoundList:
    from psychopy import core, event, logging, visual
    
    fullScreenChoice = True  # make True during actual task
    screenChoice = 0  # 2 #make 1 when only 1 monitor
    screenSize = [1920, 1080]  # make [2048, 1152]
    screenColor = "lightgray"
    textColor = "black"
    continueShapeColor = "gray"
    shapeLineColor = "black"
    # itemHeight = 0.085
    squareOutlineSize = 0.12
    squareSize = 0.1
    numColumnsPerPage = 2
    numItemsPerColumn = 10
    pauseTime = 2  # stay on item screen for 2s before skipping
    
    numSoundLabels = len(uniqueSoundLabels)
    numItemsPerPage = numItemsPerColumn * numColumnsPerPage
    numPages = math.ceil(numSoundLabels / numItemsPerPage)  # round up if not even
    
        # --- Setup the Window ---
    win = visual.Window(
        size=screenSize,
        fullscr=fullScreenChoice,
        screen=screenChoice,
        color=screenColor,
        colorSpace="rgb",
        units="norm",
    )
    
    # find average length of labels
    labelLengths=[]
    for iLabel in uniqueSoundLabels:
        labelLengths.append(len(iLabel))
    meanLength=math.floor(sum(labelLengths)/numSoundLabels)
    if meanLength > 10:
        itemHeight = 0.08
    else:
        itemHeight = 0.085
        
    def exitOut():
        logging.flush()
        win.close()
        core.quit()
        
        
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
                text="CONTINUE", #"Click here to continue",
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
    
    if step_selectTrigger:
        import psychopy_present_item_list

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

        
        instr1='First, please choose \nthe sounds you are \n\n triggered by.\n\n\nIf none of these \nsounds are triggering, \ncontinue to the \nnext page.'
        instr2='MOST\n\n\n\n\n\n'
        instrError='Please try that again.\n\nRemember, you must select at LEAST 5 sounds.'
        
        
        doneWithMostTriggering = False
        iPage=0
        pageSeen=[False]*numPages
        mostTriggeringList=[] 
        mostTriggeringList_allPages=[[0] * numItemsPerPage] * numPages #initialize index with 0s
        initSquares=[0] * numItemsPerPage #choices from previous page
        while iPage < numPages:
            instr3='Page '+str(iPage+1)+'/'+str(numPages) 
            mostTriggeringList_page,backChosen_page=psychopy_present_item_list.presentItemList(uniqueSoundLabels, numColumnsPerPage, numItemsPerColumn, numItemsPerPage, meanLength, itemHeight, squareOutlineSize, squareSize, textColor, screenColor, continueShapeColor, shapeLineColor, win, iPage,pauseTime,instr1,instr2,'firebrick',instr3,initSquares,mostTriggeringList,doneWithMostTriggering)
            pageSeen[iPage]=True
            mostTriggeringList_allPages[iPage]=mostTriggeringList_page # if len(mostTriggeringList_page)<numItemsPerPage: #last page has fewer items, can't stack if unequal lengths
        
            if backChosen_page: #if participant chooses back button
                iPage-=1
                initSquares=mostTriggeringList_allPages[iPage]
            else:
                iPage+=1
                if iPage < numPages and pageSeen[iPage]==True:
                    initSquares=mostTriggeringList_allPages[iPage]
                else:
                    initSquares=[0] * numItemsPerPage
        
        mostTriggeringIdx_temp=np.array(mostTriggeringList_allPages)
        mostTriggeringIdx=mostTriggeringIdx_temp.flatten() #vectorizes to single column       
        for iItem in range(len(mostTriggeringIdx)):
            if mostTriggeringIdx[iItem]==1:
                mostTriggeringList.append(uniqueSoundLabels[iItem])
        
        #check to make sure enough categories were chosen, if not redo
        if len(mostTriggeringList)<5:
            presentInstructions(instrError, 1)
            
            doneWithMostTriggering=False
            iPage=0
            pageSeen=[False]*numPages
            mostTriggeringList_allPages=[[0] * numItemsPerPage] * numPages #initialize index with 0s
            initSquares=[0] * numItemsPerPage #choices from previous page
            while iPage < numPages:
                instr3='Page '+str(iPage+1)+'/'+str(numPages) 
                mostTriggeringList_page,backChosen_page=psychopy_present_item_list.presentItemList(uniqueSoundLabels, numColumnsPerPage, numItemsPerColumn, numItemsPerPage, meanLength, itemHeight, squareOutlineSize, squareSize, textColor, screenColor, continueShapeColor, shapeLineColor, win, iPage,pauseTime,instr1,instr2,'firebrick',instr3,initSquares,mostTriggeringList,doneWithMostTriggering)
                pageSeen[iPage]=True
                mostTriggeringList_allPages[iPage]=mostTriggeringList_page # if len(mostTriggeringList_page)<numItemsPerPage: #last page has fewer items, can't stack if unequal lengths
        
                if backChosen_page: #if participant chooses back button
                    iPage-=1
                    initSquares=mostTriggeringList_allPages[iPage]
                else:
                    iPage+=1
                    if iPage < numPages and pageSeen[iPage]==True:
                        initSquares=mostTriggeringList_allPages[iPage]
                    else:
                        initSquares=[0] * numItemsPerPage
            
            mostTriggeringIdx_temp=np.array(mostTriggeringList_allPages)
            mostTriggeringIdx=mostTriggeringIdx_temp.flatten() #vectorizes to single column
            mostTriggeringList=[]        
            for iItem in range(len(mostTriggeringIdx)):
                if mostTriggeringIdx[iItem]==1:
                    mostTriggeringList.append(uniqueSoundLabels[iItem])
        
        doneWithMostTriggering = True

    if step_refineTrigger:
        import psychopy_refine_item_list
        
        breakInstructions1 = ('Great! \n\nOn the next page, you will see the sounds you selected. \n\nPlease choose your TOP 5 most triggering \nsounds from this list, and rank order them from \n1 (more triggering) to 5 (less triggering).')
        instr4='Please rank the \n\nsounds you \nare triggered by. \n\n1 = more triggering\n5 = less triggering \n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page.'
        instr5='TOP 5\n\n\n\n\n\n\n\n\n\n'

        presentInstructions(breakInstructions1, 0)
        
        refinedMostTriggeringList = []
        [mostTriggeringList_refined, mostTriggering_ranks] = psychopy_refine_item_list.presentRefinedItemList(meanLength, itemHeight, squareOutlineSize, squareSize, textColor, screenColor, continueShapeColor, shapeLineColor, win, mostTriggeringList, pauseTime, instr4, instr5, "firebrick"
        )
        for iItem in range(len(mostTriggeringList)):
            if mostTriggeringList_refined[iItem] == 1:
                refinedMostTriggeringList.append(
                    [mostTriggering_ranks[iItem], mostTriggeringList[iItem]]
                )
        
        refinedMostTriggeringList = sorted(refinedMostTriggeringList)
        
    if step_selectNeutral:
        breakInstructions2 = ('Next, you will repeat this process with sounds \nyou find the LEAST triggering or MOST NEUTRAL.')
        instr6='Now, please choose \nthe sounds you \nfind most\n\n\n\nIf all of these sounds\nare triggering, \ncontinue to the \nnext page.'
        instr7='\nNEUTRAL\n\n\n\n\n'
        

        presentInstructions(breakInstructions2, 0)

        
        iPage=0
        pageSeen=[False]*numPages
        leastTriggeringList_allPages=[[0] * numItemsPerPage] * numPages #initialize index with 0s
        initSquares=[0] * numItemsPerPage #choices from previous page
        while iPage < numPages:
            instr3='Page '+str(iPage+1)+'/'+str(numPages) 
            leastTriggeringList_page,backChosen_page=psychopy_present_item_list.presentItemList(uniqueSoundLabels, numColumnsPerPage, numItemsPerColumn, numItemsPerPage, meanLength, itemHeight, squareOutlineSize, squareSize, textColor, screenColor, continueShapeColor, shapeLineColor, win, iPage,pauseTime,instr6,instr7,'green',instr3,initSquares,mostTriggeringList,doneWithMostTriggering)
            pageSeen[iPage]=True
            leastTriggeringList_allPages[iPage]=leastTriggeringList_page # if len(mostTriggeringList_page)<numItemsPerPage: #last page has fewer items, can't stack if unequal lengths
        
            if backChosen_page: #if participant chooses back button
                iPage-=1
                initSquares=leastTriggeringList_allPages[iPage]
            else:
                iPage+=1
                if iPage < numPages and pageSeen[iPage]==True:
                    initSquares=leastTriggeringList_allPages[iPage]
                else:
                    initSquares=[0] * numItemsPerPage
        
        leastTriggeringIdx_temp=np.array(leastTriggeringList_allPages)
        leastTriggeringIdx=leastTriggeringIdx_temp.flatten() #vectorizes to single column
        leastTriggeringList=[]        
        for iItem in range(len(leastTriggeringIdx)):
            if leastTriggeringIdx[iItem]==1:
                leastTriggeringList.append(uniqueSoundLabels[iItem])
        
        #check to make sure enough categories were chosen, if not redo
        if len(leastTriggeringList)<5:
            presentInstructions(instrError, 1)
            
            iPage=0
            pageSeen=[False]*numPages
            leastTriggeringList_allPages=[[0] * numItemsPerPage] * numPages #initialize index with 0s
            initSquares=[0] * numItemsPerPage #choices from previous page
            while iPage < numPages:
                instr3='Page '+str(iPage+1)+'/'+str(numPages) 
                leastTriggeringList_page,backChosen_page=psychopy_present_item_list.presentItemList(uniqueSoundLabels, numColumnsPerPage, numItemsPerColumn, numItemsPerPage, meanLength, itemHeight, squareOutlineSize, squareSize, textColor, screenColor, continueShapeColor, shapeLineColor, win,iPage,pauseTime,instr6,instr7,'green',instr3,initSquares,mostTriggeringList,doneWithMostTriggering)
                pageSeen[iPage]=True
                leastTriggeringList_allPages[iPage]=leastTriggeringList_page # if len(mostTriggeringList_page)<numItemsPerPage: #last page has fewer items, can't stack if unequal lengths
        
                if backChosen_page: #if participant chooses back button
                    iPage-=1
                    initSquares=leastTriggeringList_allPages[iPage]
                else:
                    iPage+=1
                    if iPage < numPages and pageSeen[iPage]==True:
                        initSquares=leastTriggeringList_allPages[iPage]
                    else:
                        initSquares=[0] * numItemsPerPage
            
            leastTriggeringIdx_temp=np.array(leastTriggeringList_allPages)
            leastTriggeringIdx=leastTriggeringIdx_temp.flatten() #vectorizes to single column
            leastTriggeringList=[]        
            for iItem in range(len(leastTriggeringIdx)):
                if leastTriggeringIdx[iItem]==1:
                    leastTriggeringList.append(uniqueSoundLabels[iItem])
                    
    if step_refineNeutral:
        
        instr8='Please rank the \n\nsounds to you. \n\n1 = more neutral\n5 = less neutral \n\n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page.'
        instr9='5 MOST NEUTRAL\n\n\n\n\n\n\n\n\n\n'
        
        refinedLeastTriggeringList = []
        [leastTriggeringList_refined, leastTriggering_ranks] = psychopy_refine_item_list.presentRefinedItemList(meanLength, itemHeight, squareOutlineSize, squareSize, textColor, screenColor, continueShapeColor, shapeLineColor, win, leastTriggeringList, pauseTime, instr8, instr9, "green")
        for iItem in range(len(leastTriggeringList)):
            if leastTriggeringList_refined[iItem] == 1:
                refinedLeastTriggeringList.append(
                    [leastTriggering_ranks[iItem], leastTriggeringList[iItem]]
                )
        
        refinedLeastTriggeringList = sorted(refinedLeastTriggeringList)

        
    doneInstructions = ('Done!')
    presentInstructions(doneInstructions, 0)
    win.close()

if step_organizeSounds:
    # Make output file to save selections
    dataDir = homeDir + os.sep + 'Sound_Selections' + os.sep
    if not os.path.isdir(dataDir):
        os.makedirs(dataDir)
    filename = dataDir + participant + '.txt' 
    if os.path.isfile(filename) and participant != "TEST":
        if participant != "TEST":
            raise Exception('Sound Selections file for this participant already exists! Choose a different participant name.')
        else: 
            os.remove(filename)
   
        
    with open(filename, "w") as textfile:
        if step_refineSoundList:
            print("SOUND_TYPE\t", "RANK\t", "SOUND_LABEL\t\t", "FILE_NAME(S)", file=textfile)
        else:
            print("SOUND_TYPE\t", "SOUND_LABEL\t\t", "FILE_NAME(S)", file=textfile)

    # Cycle through selections to grab path names
    if step_selectTrigger:
        mostTriggerPaths = []
        rankPos = 0
        for iMost in mostTriggeringList:
            # currPath = allSoundFiles[np.char.find(allSoundLabels,iMost) >= 0][0] #find returns -1 for paths not containing the label
            currPath = allSoundFiles[np.char.find(allSoundLabels,iMost) >= 0]
            with open(filename, "a") as textfile:
                if step_refineTrigger:
                    print(
                        "Trigger\t\t",
                        str(round(mostTriggering_ranks[rankPos])) + "\t",
                        iMost + "\t\t",
                        currPath.tolist(),
                        file=textfile,
                    )
                else:
                    print(
                        "Trigger\t\t",
                        iMost + "\t\t",
                        currPath,
                        file=textfile,
                    )
            rankPos += 1

    if step_selectNeutral:
        leastTriggerPaths = []
        rankPos = 0
        for iLeast in leastTriggeringList:
            # currPath = allSoundFiles[np.char.find(allSoundLabels,iLeast) > 0][0] #find returns -1 for paths not containing the label
            currPath = allSoundFiles[np.char.find(allSoundLabels,iLeast) >= 0]
            with open(filename, "a") as textfile:
                if step_refineNeutral:
                    print(
                        "Neutral\t\t",
                        str(round(leastTriggering_ranks[rankPos])) + "\t",
                        iLeast + "\t\t",
                        currPath.tolist(),
                        file=textfile,
                    )
                else:
                    print(
                        "Neutral\t\t",
                        iLeast + "\t\t",
                        currPath.tolist(),
                        file=textfile,
                    )
            rankPos += 1

    
print("****************** Misosoupy is finished!")

