# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:16:40 2024

@author: heath
"""
from __future__ import division

import time


# --- Import packages ---
from psychopy import core, event, visual, logging

def function_exit_out(win):
    """Safely exit out of presentation, closing window and flushing log."""

    logging.flush()
    win.close()
    core.quit()
       
def function_present_item_list(unique_sound_labels, 
                    num_columns_per_page, 
                    num_items_per_column, 
                    num_items_per_page, 
                    mean_length, 
                    setup_item_height, 
                    setup_square_outline_size, 
                    setup_square_size,
                    setup_text_color, 
                    setup_screen_color,
                    setup_continue_shape_color,
                    setup_shape_line_color, 
                    win, 
                    page_num, 
                    pause_time, 
                    instructions1, 
                    instructions2, 
                    instructions2_color, 
                    instructions3, 
                    initial_squares, 
                    most_triggering_list, 
                    done_with_most_triggering):
    """Present list of sound labels onscreen for participant selection. 
        If step_select_trigger is true, participants will be instructed to select sounds that are the most triggering.
        If step_select_neutral is true, participants will be instructed to select sounds that are the most neutral (i.e., least triggering).
        Input parameters are defined within run_misosoupy.py.

    Parameters
    ----------
    unique_sound_labels : np.array
        List of sound labels to present onscreen, defined in import_sound_list.py 
    num_columns_per_page : int
        Default is 2.
    num_items_per_column : int
        Default is 10.
    num_items_per_page : int
        Default is 20. 
    mean_length : int
        Average number of characters comprising the sound labels. Used to determine font size.
    setup_item_height : int
        Font height. Default is 0.085.
    setup_square_outline_size : int
        Default is 0.12.
    setup_square_size : int
        Default is 0.1.
    setup_text_color : str
        Default is "black".
    setup_screen_color : str
        Default is "lightgray".
    setup_continue_shape_color : str
        Default is "gray".
    setup_shape_line_color : str
        Default is "black".
    win : visual.Window object
        Screen set up.
    page_num : int
        Current page number.
    pause_time : int
        How long to pause on each page before continue button appears. Default is 2 (seconds).
    instructions1 : str
        Task instructions, written in black.
    instructions2 : str
        Instruction word to emphasize (e.g., MOST, LEAST), written in color.
    instructions2_color: str
        Default is 'firebrick' for MOST, 'green' for LEAST.
    instructions3 : str
        Page counter (e.g., Page 1/5) 
    initial_squares : array
        If page was previously viewed, which squares were initially selected.
        Default: 0s for size of num_items_per_page 
    most_triggering_list : array
        List of selected trigger sounds to be grayed out during neutral sound selection.
        Starts as empty and updates as script progresses.
    done_with_most_triggering : bool
        Starts as False and updates to True after trigger selection.
    
    Returns
    -------
    items_chosen : list
        Record of which items on each page were selected (1) vs. not selected (0).
        Length will equal num_items_per_page. Resets for each page.
    back_chosen : bool
        Whether or not participant selected the BACK button.
        Default is False. If True, screen returns to previous page, maintaining selections.
    """
    
    x_position_center = (
        2 / num_columns_per_page
    ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
    y_position_center = (
        (num_items_per_column * setup_item_height) / 2
    ) + setup_item_height * 4.5  # items*height gives total screen needed, /2 to split equally b/w top and bottom half of screen

    all_word_position_values = []
    all_square_position_values = []
    for iXpos in range(num_columns_per_page):
        current_x_position = (
           x_position_center + 0.1 + 0.65 * (iXpos) 
        )  # first column starts at center, next shifts right
        for iYpos in range(num_items_per_column):
            current_y_position = (
                y_position_center
                - (setup_square_outline_size / 2)
                - setup_square_outline_size * 1.25 * (iYpos)
            )

            all_word_position_values.append((current_x_position + 0.3, current_y_position))  
            all_square_position_values.append((current_x_position - 0.25, current_y_position))

    current_page_items = unique_sound_labels[
        0 + page_num * num_items_per_page : num_items_per_page + page_num * num_items_per_page
    ]
    all_screen_words = []
    all_boxes = []
    for iItem in range(0, len(current_page_items)):
        if len(current_page_items[iItem]) > mean_length: # for long labels, decrease font size
            current_item_height=setup_item_height-0.005
        else:
            current_item_height=setup_item_height
        if len(current_page_items[iItem]) > mean_length*2: # for really long labels, put on two lines
            current_item_height=current_item_height-0.005
            current_item_text_temp=current_page_items[iItem].replace("_", " ")
            current_space_index=[i for i in range(len(current_item_text_temp)) if current_item_text_temp.startswith(" ",i)]
            if len(current_space_index) > 4:
                current_item_break_point=current_space_index[3] #break on 4th space
            else:
                current_item_break_point=current_space_index[-1] #break on last space
            current_item_text=current_item_text_temp[:current_item_break_point] + '\n\t' + current_item_text_temp[current_item_break_point:]
        else:
            current_item_text=current_page_items[iItem].replace("_", " ")
        if done_with_most_triggering:
            if (
                current_page_items[iItem] in most_triggering_list
            ):  # make sounds already chosen unclickable
                all_screen_words.append(
                    visual.TextStim(
                        win,
                        text=current_item_text,
                        pos=all_word_position_values[iItem],
                        color="gray",
                        height=current_item_height,
                        alignText="Left",
                    )
                )
                all_boxes.append(
                    visual.ShapeStim(
                        win,
                        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                        pos=all_square_position_values[iItem],
                        size=(0, 0),
                        opacity=100,
                        fillColor=None,
                        lineColor=setup_shape_line_color,
                        lineWidth=3.0,
                    )
                )
            else:
                all_screen_words.append(
                    visual.TextStim(
                        win,
                        text=current_item_text,
                        pos=all_word_position_values[iItem],
                        color=setup_text_color,
                        height=current_item_height,
                        alignText="Left",
                    )
                )
                all_boxes.append(
                    visual.ShapeStim(
                        win,
                        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                        pos=all_square_position_values[iItem],
                        size=(setup_square_size * 0.5, setup_square_size * 1.5),
                        opacity=100,
                        fillColor=None,
                        lineColor=setup_shape_line_color,
                        lineWidth=3.0,
                    )
                )
        else:
            all_screen_words.append(
                visual.TextStim(
                    win,
                    text=current_item_text,
                    pos=all_word_position_values[iItem],
                    color=setup_text_color,
                    height=current_item_height,
                    alignText="Left",
                )
            )
            all_boxes.append(
                visual.ShapeStim(
                    win,
                    vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                    pos=all_square_position_values[iItem],
                    size=(setup_square_size * 0.5, setup_square_size * 1.5),
                    opacity=100,
                    fillColor=None,
                    lineColor=setup_shape_line_color,
                    lineWidth=3.0,
                )
            )

    # # Prep Continue Button
    stim_text_instruction1 = visual.TextStim(
        win, text=instructions1, pos=(-0.7, 0.1), color=setup_text_color, height=0.09, wrapWidth=6
    )
    stim_text_instruction2 = visual.TextStim(
        win, text=instructions2, pos=(-0.7, 0.05), color=instructions2_color, height=0.09, wrapWidth=6
    )
    stim_text_instruction3 = visual.TextStim(
        win, text=instructions3, pos=(-0.7, -0.85), color=setup_text_color, height=0.09, wrapWidth=6
    )
    stim_text_continue = visual.TextStim(
        win,
        text="CONTINUE", 
        pos=(0.7, -0.85),
        color=setup_screen_color,
        height=0.08,
    )
    stim_text_back = stim_text_continue
    stim_shape_exit = visual.ShapeStim(
        win,
        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
        pos=(.75, 0.9),
        size=(0.35, 0.2),
        opacity=100,
        fillColor=setup_screen_color,
        lineColor=setup_shape_line_color,
        lineWidth=4.0,
        name="stim_shape_exit",
    )
    stim_text_exit = visual.TextStim(
        win,
        text="EXIT", 
        pos=(.75, 0.9),
        color=setup_text_color,
        height=0.08,
    )
    stim_shape_continue = stim_shape_exit
    stim_shape_back = stim_shape_exit
    
    # If page has been completed, re-present choices
    if len(initial_squares) > 0:
        for i in range(len(initial_squares)):
            if initial_squares[i]==1:
                all_boxes[i]=visual.ShapeStim(win, vertices=((-.5, -.3), (-.5, .3), (.5, .3), (.5, -.3)), pos=all_square_position_values[i], size=(setup_square_size*.5,setup_square_size*1.5), opacity=100, fillColor=setup_shape_line_color, lineColor=setup_shape_line_color,lineWidth=3.0)
        items_chosen = initial_squares
    else:
        items_chosen = [0 for i in range(len(current_page_items))]

    mouse = event.Mouse(win=win, visible=True)
    mouse.clickReset()
    event.clearEvents()
    previous_mouse_down = False

    item_clicked = False
    continue_chosen = False
    back_chosen = False
    start_time = time.time()
    while continue_chosen is False and back_chosen == False:
        for i in all_screen_words:
            i.draw()
        for j in all_boxes:
            j.draw()
        stim_text_instruction1.draw()
        stim_text_instruction2.draw()
        stim_text_instruction3.draw()
        stim_shape_back.draw()
        stim_text_back.draw()
        stim_shape_continue.draw()
        stim_text_continue.draw()
        stim_shape_exit.draw()
        stim_text_exit.draw()
        win.flip()

        if mouse.isPressedIn(stim_shape_exit):
            function_exit_out(win)   

        # Check for checkbox clicks
        for s in range(0, len(all_boxes)):
            if mouse.isPressedIn(all_boxes[s]):
                mouse_down = mouse.getPressed()[0]
                if (
                    mouse_down and not previous_mouse_down
                ):  # Only add to list if new click (otherwise, outputs each time frame refreshes, even if in the same button click)
                    if items_chosen[s] == 0:  # item hasn't been chosen yet
                        if item_clicked is False:
                            item_clicked = True
                        items_chosen[s] = 1
                        all_boxes[s] = visual.ShapeStim(
                            win,
                            vertices=(
                                (-0.5, -0.3),
                                (-0.5, 0.3),
                                (0.5, 0.3),
                                (0.5, -0.3),
                            ),
                            pos=all_square_position_values[s],
                            size=(setup_square_size * 0.5, setup_square_size * 1.5),
                            opacity=100,
                            fillColor=setup_shape_line_color,
                            lineColor=setup_shape_line_color,
                            lineWidth=3.0,
                        )
                        core.wait(0.01)  # reset button press
                    elif (
                        items_chosen[s] == 1
                    ):  # item was already chosen and is being de-selected
                        items_chosen[s] = 0
                        all_boxes[s] = visual.ShapeStim(
                            win,
                            vertices=(
                                (-0.5, -0.3),
                                (-0.5, 0.3),
                                (0.5, 0.3),
                                (0.5, -0.3),
                            ),
                            pos=all_square_position_values[s],
                            size=(setup_square_size * 0.5, setup_square_size * 1.5),
                            opacity=100,
                            fillColor=None,
                            lineColor=setup_shape_line_color,
                            lineWidth=3.0,
                        )
                    previous_mouse_down = mouse_down
                    mouse.clickReset()
                    event.clearEvents()
                    core.wait(0.25)
                    previous_mouse_down = False

        # Make Continue Button visible after 1s
        curr_time = time.time()
        if curr_time - start_time > pause_time:
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
            for i in all_screen_words:
                i.draw()
            for j in all_boxes:
                j.draw()
            stim_text_instruction1.draw()
            stim_text_instruction2.draw()
            stim_text_instruction3.draw()
            continue_chosen = True
            stim_shape_continue.draw()
            stim_text_continue.draw()
            stim_shape_exit.draw()
            stim_text_exit.draw()
            win.flip()
            
        if page_num != 0: #after first page, give option to go back to previous
            stim_text_back = visual.TextStim(win, text='BACK', pos=(x_position_center-.05, -.85), color='white', height=0.08) 
            stim_shape_back = visual.ShapeStim(win, vertices=((-.5, -.3), (-.5, .3), (.5, .3), (.5, -.3)), pos=(x_position_center-.05, -.85), size=(.25, .2), opacity=100, fillColor='black', lineColor=setup_shape_line_color,lineWidth=4.0,name='stim_shape_continue')
        
            if mouse.isPressedIn(stim_shape_back):
                for i in all_screen_words:
                    i.draw()
                for j in all_boxes:
                    j.draw()
                stim_text_instruction1.draw()
                stim_text_instruction2.draw()
                stim_text_instruction3.draw()    
                back_chosen = True
                stim_shape_continue.draw()
                stim_text_continue.draw()
                stim_shape_exit.draw()
                stim_text_exit.draw()
                win.flip()     

    return items_chosen, back_chosen  # results are a list of 0s and 1s
