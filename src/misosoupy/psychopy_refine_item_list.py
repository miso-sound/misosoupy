# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:38:17 2024

@author: heath
"""

from __future__ import division

import math

import numpy as np

import os

# --- Import packages ---
from psychopy import core, event, logging, visual

# Import config file and screen parameters
import setup_misosoupy
config_path = setup_misosoupy.get_home_dir() + os.sep + 'config.ini'
[setup_steps, setup_screen]=setup_misosoupy.parse_config_file(config_path)

setup_square_outline_size = setup_screen.get('setup_square_outline_size')
setup_square_size = setup_screen.get('setup_square_size')
setup_text_color = setup_screen.get('setup_text_color')
setup_screen_color = setup_screen.get('setup_screen_color')
setup_continue_shape_color = setup_screen.get('setup_continue_shape_color')
setup_shape_line_color = setup_screen.get('setup_shape_line_color')

def function_exit_out(win):
    """Safely exit out of presentation, closing window and flushing log."""

    logging.flush()
    win.close()
    core.quit()


def function_present_refined_item_list(
    mean_length,
    setup_item_height,
    win,
    items,
    instructions1,
    instructions2,
    instructions2_color,
):
    """Present all participant selections onscreen for further refinement.
        If step_refine_trigger is true, participants will refine their trigger sound selections.
        If step_refine_neutral is true, participants will refined their neutral sound selections.
        Input parameters are defined within run_misosoupy.py.

    Parameters
    ----------
    mean_length : int
        Average number of characters comprising the sound labels. Used to determine font size.
    setup_item_height : int
        Font height. Default is 0.085.
    win : visual.Window object
        Screen set up.
    items : list
        Sound labels selected during psychopy_present_item_list.py.
    instructions1 : str
        Task instructions, written in black.
    instructions2 : str
        Instruction word(s) to emphasize (e.g., MOST, LEAST), written in color.
    instructions2_color: str
        Default is 'firebrick' for MOST, 'green' for LEAST.

    Returns
    -------
    items_chosen : list
        Record of which items on each page were selected (1) vs. not selected (0).
        Length will equal length of "items".
    all_ranks : numpy array
        Record of ranks assigned to each item.
        Length will equal length of "items", with 0s for un-selected items and chosen rank (e.g., 1-5) for selected items.
    """

    # Determine how many rows/columns are needed
    num_items = len(items)
    if num_items <= 12:
        num_columns = 1
        num_rows = num_items
        refined_item_height = setup_item_height
        x_position_center = 0  #
        column_gap = 0.6
    elif num_items > 12 and num_items <= 24:
        num_columns = 2
        num_rows = math.ceil(num_items / 2)
        x_position_center = (
            2 / num_columns
        ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
        refined_item_height = setup_item_height
        column_gap = 0.6
    elif num_items > 24 and num_items <= 36:
        num_columns = 3
        num_rows = math.ceil(num_items / 3)
        refined_item_height = 0.075
        x_position_center = (
            2 / num_columns
        ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
        column_gap = 0.45
    elif num_items > 36:
        num_columns = 4
        num_rows = math.ceil(num_items / 4)
        refined_item_height = 0.065
        x_position_center = (
            2 / num_columns
        ) / 2 - 0.5 * 1.25  # 2/ since distance of screen units (+1-->-1), /2 for middle of word, *1.5 for scale
        column_gap = 0.35

    y_position_center = ((num_rows * refined_item_height) / 2) + refined_item_height * 5
    # items*height gives total screen needed, /2 to split equally b/w top and bottom half of screen

    all_word_position_values = []
    all_square_position_values = []
    for iXpos in range(num_columns):
        current_x_position = (
            x_position_center + 0.1 + column_gap * (iXpos)
        )  # first column starts at center, next shifts right
        for iYpos in range(num_rows):
            current_y_position = (
                y_position_center
                - (setup_square_outline_size / 2)
                - setup_square_outline_size * 1.25 * (iYpos)
            )

            all_word_position_values.append(
                (current_x_position + (0.35), current_y_position)
            )
            all_square_position_values.append(
                (current_x_position - 0.2, current_y_position)
            )

    all_screen_words = []
    all_boxes = []
    all_choices = []
    for iItem in range(0, len(items)):
        if (
            num_columns > 1 and len(items[iItem]) > mean_length
        ):  # for long labels, decrease font size
            current_item_height = refined_item_height - 0.005  # 0.01
        else:
            current_item_height = refined_item_height
        if (
            len(items[iItem]) > mean_length * 2
        ):  # for really long labels, put on two lines
            current_item_height = current_item_height - 0.005
            current_item_text_temp = items[iItem].replace("_", " ")
            current_space_index = [
                i
                for i in range(len(current_item_text_temp))
                if current_item_text_temp.startswith(" ", i)
            ]
            if len(current_space_index) > 4:
                current_item_break_point = current_space_index[3]  # break on 4th space
            else:
                current_item_break_point = current_space_index[
                    -1
                ]  # break on last space
            current_item_text = (
                current_item_text_temp[:current_item_break_point]
                + "\n\t"
                + current_item_text_temp[current_item_break_point:]
            )
        else:
            current_item_text = items[iItem].replace("_", " ")
        all_screen_words.append(
            visual.TextStim(
                win,
                text=current_item_text,
                pos=all_word_position_values[iItem],
                color=instructions2_color,
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
        all_choices.append(
            visual.TextStim(
                win,
                text=" ",
                color=setup_text_color,
                height=refined_item_height,
                bold=True,
            )
        )

    # # Prep Continue Button
    stim_text_instruction1 = visual.TextStim(
        win,
        text=instructions1,
        pos=(-0.7, 0.1),
        color=setup_text_color,
        height=0.09,
        wrapWidth=6,
    )
    stim_text_instruction2 = visual.TextStim(
        win,
        text=instructions2,
        pos=(-0.7, 0.05),
        color=instructions2_color,
        height=0.09,
        wrapWidth=6,
    )
    stim_text_continue = visual.TextStim(
        win,
        text="CONTINUE",
        pos=(0.7, -0.85),
        color=setup_screen_color,
        height=0.08,
    )
    stim_shape_exit = visual.ShapeStim(
        win,
        vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
        pos=(0.75, 0.9),
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
        pos=(0.75, 0.9),
        color=setup_text_color,
        height=0.08,
    )
    stim_shape_reset = stim_shape_exit  # just temp placeholders
    stim_text_reset = stim_text_continue
    stim_shape_continue = stim_shape_exit

    mouse = event.Mouse(win=win, visible=True)
    mouse.clickReset()
    event.clearEvents()
    previous_mouse_down = False

    all_ranks_chosen = False
    current_rank = 1  # 0
    continue_chosen = False
    items_chosen = [0 for i in range(len(items))]
    while continue_chosen is False:
        for i in all_screen_words:
            i.draw()
        for j in all_boxes:
            j.draw()
        for c in all_choices:
            c.draw()
        stim_text_instruction1.draw()
        stim_text_instruction2.draw()
        stim_shape_continue.draw()
        stim_text_continue.draw()
        stim_shape_reset.draw()
        stim_text_reset.draw()
        stim_shape_exit.draw()
        stim_text_exit.draw()
        win.flip()

        if mouse.isPressedIn(stim_shape_exit):
            function_exit_out()

        # Check for checkbox clicks
        for s in range(0, len(all_boxes)):
            if mouse.isPressedIn(all_boxes[s]):
                mouse_down = mouse.getPressed()[0]
                if (
                    mouse_down and not previous_mouse_down
                ):  # Only add to list if new click
                    # (otherwise, outputs each time frame refreshes, even if in the same button click)
                    if items_chosen[s] == 0:  # item hasn't been chosen yet
                        items_chosen[s] = 1
                        all_choices[s].pos = all_square_position_values[s]
                        all_choices[s].text = str(current_rank)
                        if current_rank == 5:
                            all_ranks_chosen = True
                        else:
                            current_rank += 1
                        core.wait(0.01)  # reset button press

                    elif (
                        items_chosen[s] == 1
                    ):  # item was already chosen and is being de-selected
                        items_chosen[s] = 0
                        all_choices[s].pos = (0, 0)
                        all_choices[s].text = " "
                        if current_rank > 1:
                            current_rank -= 1
                    previous_mouse_down = mouse_down
                    mouse.clickReset()
                    event.clearEvents()
                    core.wait(0.25)
                    previous_mouse_down = False

        # Make Continue Button visible after 1s

        if sum(items_chosen) != 0:  # if they've clicked something, give option to reset
            stim_text_reset = visual.TextStim(
                win, text="RESET", pos=(-0.7, -0.85), color="white", height=0.08
            )
            stim_shape_reset = visual.ShapeStim(
                win,
                vertices=((-0.5, -0.3), (-0.5, 0.3), (0.5, 0.3), (0.5, -0.3)),
                pos=(-0.7, -0.85),
                size=(0.3, 0.2),
                opacity=100,
                fillColor="black",
                lineColor=setup_shape_line_color,
                lineWidth=4.0,
                name="stim_shape_continue",
            )

        if mouse.isPressedIn(stim_shape_reset):
            items_chosen = [0 for i in range(len(items))]
            current_rank = 1
            stim_shape_continue = stim_shape_exit
            stim_text_continue = stim_text_reset
            for r in range(0, len(all_boxes)):
                all_choices[r].pos = (0, 0)
                all_choices[r].text = " "

        if all_ranks_chosen:
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
            continue_chosen = True
            stim_shape_continue.draw()
            stim_text_continue.draw()
            stim_shape_exit.draw()
            stim_text_exit.draw()
            win.flip()

    all_ranks = np.zeros(len(all_choices))
    for i in range(len(all_choices)):
        current_item_rank = all_choices[i].text
        if current_item_rank != " ":
            all_ranks[i] = int(current_item_rank)

    return items_chosen, all_ranks  # results are a list of 0s and 1s
