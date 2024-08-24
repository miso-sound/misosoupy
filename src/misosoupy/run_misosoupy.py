# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:02:55 2024

@author: heath

THINGS TO STILL ADD (AUG 23 2024):
    
    Option to set minimum required sounds (current default: 5 per category)
    Option to change instructions?
    Option to change colors
    Option to select sounds without needing psychopy?


"""

from __future__ import division

import math
import os  # handy system and path functions

import numpy as np

# Set up preferences ################
step_import_sound_list = True
step_select_sound_list = True
step_select_trigger, step_select_neutral = True, True
step_refine_sound_list = True
step_refine_trigger, step_refine_neutral = True, True
step_organize_sounds = True

# Setup paths and IDs
import setup_misosoupy
global home_dir
home_dir=setup_misosoupy.get_home_dir() #creates global variable "home_dir"
global participant
participant=setup_misosoupy.get_participant_id() #creates global variable "participant"
global source_sound_list
source_sound_list=setup_misosoupy.get_sound_list() #creates global variable "source_sound_list"


if step_import_sound_list:
    import import_sound_list
    [all_sound_files, all_sound_labels, unique_sound_labels]=import_sound_list.function_import_sound_list(home_dir,source_sound_list) #'naturalsounds165' sound_list.csv
else:
    raise Exception("Need sounds to select from!")    
    
if step_select_sound_list or step_refine_sound_list:
    from psychopy import core, event, logging, visual
    
    setup_full_screen_choice = True  # make True during actual task
    setup_which_screen = 0  # 2 #make 1 when only 1 monitor
    setup_screen_size = [1920, 1080]  # make [2048, 1152]
    setup_screen_color = "lightgray"
    setup_text_color = "black"
    setup_continue_shape_color = "gray"
    setup_shape_line_color = "black"
    setup_square_outline_size = 0.12
    setup_square_size = 0.1
    num_columns_per_page = 2
    num_items_per_column = 10
    pause_time = 2  # stay on item screen for 2s before skipping
    
    num_sound_labels = len(unique_sound_labels)
    num_items_per_page = num_items_per_column * num_columns_per_page
    num_pages = math.ceil(num_sound_labels / num_items_per_page)  # round up if not even
    
        # --- Setup the Window ---
    win = visual.Window(
        size=setup_screen_size,
        fullscr=setup_full_screen_choice,
        screen=setup_which_screen,
        color=setup_screen_color,
        colorSpace="rgb",
        units="norm",
    )
    
    # find average length of labels
    label_lengths=[]
    for iLabel in unique_sound_labels:
        label_lengths.append(len(iLabel))
    mean_length=math.floor(sum(label_lengths)/num_sound_labels)
    if mean_length > 10:
        setup_item_height = 0.08
    else:
        setup_item_height = 0.085
        
    def function_exit_out():
        """Safely exit out of presentation, closing window and flushing log."""

        logging.flush()
        win.close()
        core.quit()
        
        
    def function_present_instructions(instruction_text, wait_time):
        """ Present instruction text onscreen using PsychoPy. 

        Parameters
        ----------
        instruction_text : str
            Text to display.
        wait_time : int
            Time (in seconds) to pause before CONTINUE button is displayed.
        """

        # Prep instructions
        stim_text_instruction1 = visual.TextStim(
            win, text=instruction_text, pos=(0, 0), color=setup_text_color, height=0.09, wrapWidth=6
        )
        # Prep Continue Button
        stim_text_continue = visual.TextStim(
            win,
            text="Click here to continue",
            pos=(0.7, -0.85),
            color=setup_screen_color,
            height=0.08,
        )
        stim_shape_exit = visual.ShapeStim(
            win,
            vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
            pos=(1, 1),
            size=(0.35, 0.35),
            opacity=100,
            fillColor=setup_screen_color,
            lineColor=None,
            lineWidth=4.0,
            name="stim_shape_exit",
        )
        stim_shape_continue = stim_shape_exit
    
        mouse = event.Mouse(win=win, visible=True)
        mouse.clickReset()
        event.clearEvents()
    
        continue_chosen = False
        stim_text_instruction1.draw()
        stim_shape_continue.draw()
        stim_text_continue.draw()
        stim_shape_exit.draw()
        win.flip()
        core.wait(wait_time)
        while continue_chosen is False:
            stim_text_instruction1.draw()
            stim_shape_continue.draw()
            stim_text_continue.draw()
            stim_shape_exit.draw()
            win.flip()
    
            if mouse.isPressedIn(stim_shape_exit):
                function_exit_out()
    
            # Make Continue Button visible after 3 seconds
            stim_shape_continue = visual.ShapeStim(
                win,
                vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                pos=(0.7, -0.85),
                size=(0.45, 0.2),
                opacity=100,
                fillColor=setup_continue_shape_color,
                lineColor=setup_shape_line_color,
                lineWidth=4.0,
                name="stim_shape_continue",
            )
            stim_text_continue = visual.TextStim(
                win,
                text="CONTINUE", 
                pos=(0.7, -0.85),
                color=setup_text_color,
                height=0.08,
            )
    
            if mouse.isPressedIn(stim_shape_continue):
                stim_text_instruction1.draw()
                stim_shape_continue.draw()
                stim_text_continue.draw()
                win.flip()
                continue_chosen = True
    
    if step_select_trigger:
        import psychopy_present_item_list

        instructions_general = (
            "In this experiment, you will listen to sounds."
            + "\nIt is important that we use the most effective sounds for each participant."
            + "\n\nOn the next pages, you will see the names of sounds. \nPlease select the sounds "
            + "that you find \nthe MOST triggering (e.g., bothersome, unpleasant) "
            + "and \nthe LEAST triggering (e.g., neutral, neither pleasant nor unpleasant)."
            + "\nDo this by clicking the box next to the sound name."
            + "\n\nThere will be 5 pages for each prompt (most and least). \nTry to choose AT LEAST 4-5 sounds for each prompt."
        )
        function_present_instructions(instructions_general, 1)

        
        instructions1='First, please choose \nthe sounds you are \n\n triggered by.\n\n\nIf none of these \nsounds are triggering, \ncontinue to the \nnext page.'
        instructions2='MOST\n\n\n\n\n\n'
        instructions_error='Please try that again.\n\nRemember, you must select at LEAST 5 sounds.'
        
        
        done_with_most_triggering = False
        iPage=0
        page_seen=[False]*num_pages
        most_triggering_list=[] 
        most_triggering_list_all_pages=[[0] * num_items_per_page] * num_pages #initialize index with 0s
        initial_squares=[0] * num_items_per_page #choices from previous page
        while iPage < num_pages:
            instructions3='Page '+str(iPage+1)+'/'+str(num_pages) 
            most_triggering_list_page,back_chosen_page=psychopy_present_item_list.function_present_item_list(unique_sound_labels, num_columns_per_page, num_items_per_column, num_items_per_page, mean_length, setup_item_height, setup_square_outline_size, setup_square_size, setup_text_color, setup_screen_color, setup_continue_shape_color, setup_shape_line_color, win, iPage,pause_time,instructions1,instructions2,'firebrick',instructions3,initial_squares,most_triggering_list,done_with_most_triggering)
            page_seen[iPage]=True
            most_triggering_list_all_pages[iPage]=most_triggering_list_page 
        
            if back_chosen_page: #if participant chooses back button
                iPage-=1
                initial_squares=most_triggering_list_all_pages[iPage]
            else:
                iPage+=1
                if iPage < num_pages and page_seen[iPage]==True:
                    initial_squares=most_triggering_list_all_pages[iPage]
                else:
                    initial_squares=[0] * num_items_per_page
        
        most_triggering_index_temp=np.array(most_triggering_list_all_pages)
        most_triggering_index=most_triggering_index_temp.flatten() #vectorizes to single column       
        for iItem in range(len(most_triggering_index)):
            if most_triggering_index[iItem]==1:
                most_triggering_list.append(unique_sound_labels[iItem])
        
        #check to make sure enough categories were chosen, if not redo
        if len(most_triggering_list)<5:
            function_present_instructions(instructions_error, 1)
            
            done_with_most_triggering=False
            iPage=0
            page_seen=[False]*num_pages
            most_triggering_list_all_pages=[[0] * num_items_per_page] * num_pages #initialize index with 0s
            initial_squares=[0] * num_items_per_page #choices from previous page
            while iPage < num_pages:
                instructions3='Page '+str(iPage+1)+'/'+str(num_pages) 
                most_triggering_list_page,back_chosen_page=psychopy_present_item_list.function_present_item_list(unique_sound_labels, num_columns_per_page, num_items_per_column, num_items_per_page, mean_length, setup_item_height, setup_square_outline_size, setup_square_size, setup_text_color, setup_screen_color, setup_continue_shape_color, setup_shape_line_color, win, iPage,pause_time,instructions1,instructions2,'firebrick',instructions3,initial_squares,most_triggering_list,done_with_most_triggering)
                page_seen[iPage]=True
                most_triggering_list_all_pages[iPage]=most_triggering_list_page 
        
                if back_chosen_page: #if participant chooses back button
                    iPage-=1
                    initial_squares=most_triggering_list_all_pages[iPage]
                else:
                    iPage+=1
                    if iPage < num_pages and page_seen[iPage]==True:
                        initial_squares=most_triggering_list_all_pages[iPage]
                    else:
                        initial_squares=[0] * num_items_per_page
            
            most_triggering_index_temp=np.array(most_triggering_list_all_pages)
            most_triggering_index=most_triggering_index_temp.flatten() #vectorizes to single column
            most_triggering_list=[]        
            for iItem in range(len(most_triggering_index)):
                if most_triggering_index[iItem]==1:
                    most_triggering_list.append(unique_sound_labels[iItem])
        
        done_with_most_triggering = True

    if step_refine_trigger:
        import psychopy_refine_item_list
        
        instructions_break1 = ('Great! \n\nOn the next page, you will see the sounds you selected. \n\nPlease choose your TOP 5 most triggering \nsounds from this list, and rank order them from \n1 (more triggering) to 5 (less triggering).')
        instructions4='Please rank the \n\nsounds you \nare triggered by. \n\n1 = more triggering\n5 = less triggering \n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page.'
        instructions5='TOP 5\n\n\n\n\n\n\n\n\n\n'

        function_present_instructions(instructions_break1, 0)
        
        refined_most_triggering_list = []
        [most_triggering_list_refined, most_triggering_ranks] = psychopy_refine_item_list.function_present_refined_item_list(mean_length, setup_item_height, setup_square_outline_size, setup_square_size, setup_text_color, setup_screen_color, setup_continue_shape_color, setup_shape_line_color, win, most_triggering_list, instructions4, instructions5, "firebrick"
        )
        for iItem in range(len(most_triggering_list)):
            if most_triggering_list_refined[iItem] == 1:
                refined_most_triggering_list.append(
                    [most_triggering_ranks[iItem], most_triggering_list[iItem]]
                )
        
        refined_most_triggering_list = sorted(refined_most_triggering_list)
        
    if step_select_neutral:
        instructions_break2 = ('Next, you will repeat this process with sounds \nyou find the LEAST triggering or MOST NEUTRAL.')
        instructions6='Now, please choose \nthe sounds you \nfind most\n\n\n\nIf all of these sounds\nare triggering, \ncontinue to the \nnext page.'
        instructions7='\nNEUTRAL\n\n\n\n\n'
        

        function_present_instructions(instructions_break2, 0)

        
        iPage=0
        page_seen=[False]*num_pages
        least_triggering_list_all_pages=[[0] * num_items_per_page] * num_pages #initialize index with 0s
        initial_squares=[0] * num_items_per_page #choices from previous page
        while iPage < num_pages:
            instructions3='Page '+str(iPage+1)+'/'+str(num_pages) 
            least_triggering_list_page,back_chosen_page=psychopy_present_item_list.function_present_item_list(unique_sound_labels, num_columns_per_page, num_items_per_column, num_items_per_page, mean_length, setup_item_height, setup_square_outline_size, setup_square_size, setup_text_color, setup_screen_color, setup_continue_shape_color, setup_shape_line_color, win, iPage,pause_time,instructions6,instructions7,'green',instructions3,initial_squares,most_triggering_list,done_with_most_triggering)
            page_seen[iPage]=True
            least_triggering_list_all_pages[iPage]=least_triggering_list_page 
        
            if back_chosen_page: #if participant chooses back button
                iPage-=1
                initial_squares=least_triggering_list_all_pages[iPage]
            else:
                iPage+=1
                if iPage < num_pages and page_seen[iPage]==True:
                    initial_squares=least_triggering_list_all_pages[iPage]
                else:
                    initial_squares=[0] * num_items_per_page
        
        least_triggering_index_temp=np.array(least_triggering_list_all_pages)
        least_triggering_index=least_triggering_index_temp.flatten() #vectorizes to single column
        least_triggering_list=[]        
        for iItem in range(len(least_triggering_index)):
            if least_triggering_index[iItem]==1:
                least_triggering_list.append(unique_sound_labels[iItem])
        
        #check to make sure enough categories were chosen, if not redo
        if len(least_triggering_list)<5:
            function_present_instructions(instructions_error, 1)
            
            iPage=0
            page_seen=[False]*num_pages
            least_triggering_list_all_pages=[[0] * num_items_per_page] * num_pages #initialize index with 0s
            initial_squares=[0] * num_items_per_page #choices from previous page
            while iPage < num_pages:
                instructions3='Page '+str(iPage+1)+'/'+str(num_pages) 
                least_triggering_list_page,back_chosen_page=psychopy_present_item_list.function_present_item_list(unique_sound_labels, num_columns_per_page, num_items_per_column, num_items_per_page, mean_length, setup_item_height, setup_square_outline_size, setup_square_size, setup_text_color, setup_screen_color, setup_continue_shape_color, setup_shape_line_color, win,iPage,pause_time,instructions6,instructions7,'green',instructions3,initial_squares,most_triggering_list,done_with_most_triggering)
                page_seen[iPage]=True
                least_triggering_list_all_pages[iPage]=least_triggering_list_page 
        
                if back_chosen_page: #if participant chooses back button
                    iPage-=1
                    initial_squares=least_triggering_list_all_pages[iPage]
                else:
                    iPage+=1
                    if iPage < num_pages and page_seen[iPage]==True:
                        initial_squares=least_triggering_list_all_pages[iPage]
                    else:
                        initial_squares=[0] * num_items_per_page
            
            least_triggering_index_temp=np.array(least_triggering_list_all_pages)
            least_triggering_index=least_triggering_index_temp.flatten() #vectorizes to single column
            least_triggering_list=[]        
            for iItem in range(len(least_triggering_index)):
                if least_triggering_index[iItem]==1:
                    least_triggering_list.append(unique_sound_labels[iItem])
                    
    if step_refine_neutral:
        
        instructions8='Please rank the \n\nsounds to you. \n\n1 = more neutral\n5 = less neutral \n\n\nOnce you have \nselected your top 5, \ncontinue to the \nnext page.'
        instructions9='5 MOST NEUTRAL\n\n\n\n\n\n\n\n\n\n'
        
        refined_least_triggering_list = []
        [least_triggering_list_refined, least_triggering_ranks] = psychopy_refine_item_list.function_present_refined_item_list(mean_length, setup_item_height, setup_square_outline_size, setup_square_size, setup_text_color, setup_screen_color, setup_continue_shape_color, setup_shape_line_color, win, least_triggering_list, instructions8, instructions9, "green")
        for iItem in range(len(least_triggering_list)):
            if least_triggering_list_refined[iItem] == 1:
                refined_least_triggering_list.append(
                    [least_triggering_ranks[iItem], least_triggering_list[iItem]]
                )
        
        refined_least_triggering_list = sorted(refined_least_triggering_list)

        
    instructions_done = ('Done!')
    function_present_instructions(instructions_done, 0)
    win.close()

if step_organize_sounds:
    # Make output file to save selections
    data_dir = home_dir + os.sep + 'Sound_Selections' + os.sep
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    file_name = data_dir + participant + '.txt' 
    if os.path.isfile(file_name) and participant != "TEST":
        if participant != "TEST":
            raise Exception('Sound Selections file for this participant already exists! Choose a different participant name.')
        else: 
            os.remove(file_name)
   
        
    with open(file_name, "w") as textfile:
        if step_refine_sound_list:
            print("SOUND_TYPE\t", "RANK\t", "SOUND_LABEL\t\t", "FILE_NAME(S)", file=textfile)
        else:
            print("SOUND_TYPE\t", "SOUND_LABEL\t\t", "FILE_NAME(S)", file=textfile)

    # Cycle through selections to grab path names
    if step_select_trigger:
        most_trigger_paths = []
        rank_position = 0
        for iMost in most_triggering_list:
            current_path = all_sound_files[np.char.find(all_sound_labels,iMost) >= 0]
            with open(file_name, "a") as textfile:
                if step_refine_trigger:
                    print(
                        "Trigger\t\t",
                        str(round(most_triggering_ranks[rank_position])) + "\t",
                        iMost + "\t\t",
                        current_path.tolist(),
                        file=textfile,
                    )
                else:
                    print(
                        "Trigger\t\t",
                        iMost + "\t\t",
                        current_path,
                        file=textfile,
                    )
            rank_position += 1

    if step_select_neutral:
        least_trigger_paths = []
        rank_position = 0
        for iLeast in least_triggering_list:
            current_path = all_sound_files[np.char.find(all_sound_labels,iLeast) >= 0]
            with open(file_name, "a") as textfile:
                if step_refine_neutral:
                    print(
                        "Neutral\t\t",
                        str(round(least_triggering_ranks[rank_position])) + "\t",
                        iLeast + "\t\t",
                        current_path.tolist(),
                        file=textfile,
                    )
                else:
                    print(
                        "Neutral\t\t",
                        iLeast + "\t\t",
                        current_path.tolist(),
                        file=textfile,
                    )
            rank_position += 1

    
print("****************** Misosoupy is finished!")

