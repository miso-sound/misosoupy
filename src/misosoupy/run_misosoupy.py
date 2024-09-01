# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:02:55 2024

@author: heath

THINGS TO STILL ADD (AUG 23 2024):

    Option to select sounds without needing psychopy?

"""

from __future__ import division

import math
import os  
import numpy as np

"""
-------------------------------------------------------------------------------
                        Set up paths and preferences
-------------------------------------------------------------------------------
"""
# Read in paths, variables
import setup_misosoupy
global home_dir
home_dir = setup_misosoupy.get_home_dir()  # creates global variable "home_dir"
path_to_assets = setup_misosoupy.get_path_to_assets()
global participant
participant = (
    setup_misosoupy.get_participant_id()
)  # creates global variable "participant"
global source_sound_list
source_sound_list = (
    setup_misosoupy.get_sound_list(path_to_assets)
)  # creates global variable "source_sound_list"

# Read config file
[setup_steps, setup_screen]=setup_misosoupy.parse_config_file()

# Error if setup step choices are incompatible
if (setup_steps.get('step_select_sound_list') is False) and (setup_steps.get('step_select_trigger') is True or setup_steps.get('step_select_neutral') is True):
    raise Exception("To select particular sounds (e.g., trigger, neutral), make sure Step_select_sound_list = True")
if (setup_steps.get('step_select_sound_list') is False) and (setup_steps.get('step_refine_sound_list') is True):
    raise Exception("Need to select sounds before you can refine them! Make sure Step_select_sound_list = True")
if (setup_steps.get('step_refine_sound_list') is False) and (setup_steps.get('step_refine_trigger') is True or setup_steps.get('step_refine_neutral') is True):
    raise Exception("To refine particular sounds (e.g., trigger, neutral), make sure Step_refine_sound_list = True")
if (setup_steps.get('step_select_sound_list') is False) and (setup_steps.get('step_organize_sounds') is True):
    raise Exception("Need to select sounds before you can organize them! Make sure Step_select_sound_list = True")

# Error if participant number is already used, otherwise prep data file
if (setup_steps.get('step_organize_sounds') is True):
    # Make output file to save selections
    data_dir = home_dir + os.sep + "Sound_Selections" + os.sep
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    file_name = data_dir + participant + ".txt"

    usable_file_name_found = False
    while usable_file_name_found is False:
        if os.path.isfile(file_name):
            if participant == "TEST":
                os.remove(file_name)
                usable_file_name_found = True
            else:
                print("Sound Selections file for this participant already exists! Choose a different participant name.")
                
                participant = (
                    setup_misosoupy.get_participant_id()
                )  # choose a new participant id
                file_name = data_dir + participant + ".txt"

        else:
            usable_file_name_found = True

"""
-------------------------------------------------------------------------------
                        Import sound labels
-------------------------------------------------------------------------------
"""
if (setup_steps.get('step_import_sound_list') is True):
    import import_sound_list

    [all_sound_files, all_sound_labels, unique_sound_labels] = (
        import_sound_list.function_import_sound_list(path_to_assets, source_sound_list)
    )  
else:
    raise Exception("Need sounds to select from! Make sure Step_import_sound_list = True")

"""
-------------------------------------------------------------------------------
                        Present sound labels onscreen
-------------------------------------------------------------------------------
"""
if (setup_steps.get('step_select_sound_list') is True) or (setup_steps.get('step_refine_sound_list') is True):
    from psychopy import visual
    import psychopy_present_instructions
    
    setup_full_screen_choice = setup_screen.get('setup_full_screen_choice')
    setup_which_screen = setup_screen.get('setup_which_screen')
    setup_screen_color = setup_screen.get('setup_screen_color')
    setup_text_color = setup_screen.get('setup_text_color')
    setup_continue_shape_color = setup_screen.get('setup_continue_shape_color')
    setup_shape_line_color = setup_screen.get('setup_shape_line_color')
    setup_square_outline_size = setup_screen.get('setup_square_outline_size')
    setup_square_size = setup_screen.get('setup_square_size')
    num_items_to_select = setup_screen.get('num_items_to_select')
    num_columns_per_page = setup_screen.get('num_columns_per_page')
    num_items_per_column = setup_screen.get('num_items_per_column')
    pause_time = setup_screen.get('pause_time')

    num_sound_labels = len(unique_sound_labels)
    num_items_per_page = num_items_per_column * num_columns_per_page
    num_pages = math.ceil(num_sound_labels / num_items_per_page)  # round up if not even

    # --- Setup the Window ---
    win = visual.Window(
        fullscr=setup_full_screen_choice,
        screen=setup_which_screen,
        color=setup_screen_color,
        colorSpace="rgb",
        units="norm",
    )

    # find average length of labels
    label_lengths = []
    for iLabel in unique_sound_labels:
        label_lengths.append(len(iLabel))
    mean_length = math.floor(sum(label_lengths) / num_sound_labels)
    if mean_length > 10:
        setup_item_height = 0.08
    else:
        setup_item_height = 0.085

    """
    ----------- Start sound selection process --------------------------------------------------------
    """
    if (setup_steps.get('step_select_sound_list') is True):
        import psychopy_present_item_list
        
        # Prep instruction screen, depending on whether trigger/neutral/both is chosen
        instructions_general1 = (
            "In this experiment, you will listen to sounds."
            + "\nIt is important that we use the most effective sounds for each participant."
            + "\n\nOn the next pages, you will see the names of sounds."
        )
        instructions_general2 = ("\nDo this by clicking the box next to the sound name.")
        if (setup_steps.get('step_select_trigger') is True) and (setup_steps.get('step_select_neutral') is True):
            instructions_general3 = (
                "\nPlease select the sounds that you find"
                + "\nthe MOST triggering (e.g., bothersome, unpleasant) "
                + "and \nthe LEAST triggering (e.g., neutral, neither pleasant nor unpleasant)."
            )
            instructions_general4 = (
                "\n\nThere will be "
                + str(num_pages)
                + " page(s) for each prompt (most and least). "
                + "\nTry to choose AT LEAST "
                + str(num_items_to_select)
                + " sounds for each prompt."
            )
        elif (setup_steps.get('step_select_trigger') is True) and (setup_steps.get('step_select_neutral') is False):
            instructions_general3 = (
                "\nPlease select the sounds that you find"
                + "\nthe MOST triggering (e.g., bothersome, unpleasant). "
            )
            instructions_general4 = (
                "\n\nThere will be "
                + str(num_pages)
                + " page(s).\nTry to choose AT LEAST "
                + str(num_items_to_select)
                + " sounds."
            )
        elif (setup_steps.get('step_select_trigger') is False) and (setup_steps.get('step_select_neutral') is True):
            instructions_general3 = (
                "\nPlease select the sounds that you find"
                + "\nthe LEAST triggering (e.g., neutral, neither pleasant nor unpleasant)."
            )
            instructions_general4 = (
                "\n\nThere will be "
                + str(num_pages)
                + " page(s).\nTry to choose AT LEAST "
                + str(num_items_to_select)
                + " sounds."
            )
        instructions_general = instructions_general1 + instructions_general3 + instructions_general2 + instructions_general4
        psychopy_present_instructions.function_present_instructions(win, instructions_general, 1)

        instructions_error = (
            "Please try that again.\n\nRemember, you must select at LEAST "
            + str(num_items_to_select)
            + " sounds, if possible."
        )

        """
        ----------- Select trigger sounds --------------------------------------------------------
        """
        if (setup_steps.get('step_select_trigger') is True):
            instructions1 = (
                "First, please choose \nthe sounds you are \n\n triggered by."
                + "\n\n\nIf none of these \nsounds are triggering, \ncontinue to the \nnext page."
            )
            instructions2 = "MOST\n\n\n\n\n\n"

            done_with_most_triggering = False
            iPage = 0
            page_seen = [False] * num_pages
            most_triggering_list = []
            most_triggering_list_all_pages = [
                [0] * num_items_per_page
            ] * num_pages  # initialize index with 0s
            initial_squares = [0] * num_items_per_page  # choices from previous page
            while iPage < num_pages:
                instructions3 = "Page " + str(iPage + 1) + "/" + str(num_pages)
                most_triggering_list_page, back_chosen_page = (
                    psychopy_present_item_list.function_present_item_list(
                        unique_sound_labels,
                        num_items_per_page,
                        mean_length,
                        setup_item_height,
                        win,
                        iPage,
                        instructions1,
                        instructions2,
                        "firebrick",
                        instructions3,
                        initial_squares,
                        most_triggering_list,
                        done_with_most_triggering,
                    )
                )
                page_seen[iPage] = True
                most_triggering_list_all_pages[iPage] = most_triggering_list_page

                if back_chosen_page:  # if participant chooses back button
                    iPage -= 1
                    initial_squares = most_triggering_list_all_pages[iPage]
                else:
                    iPage += 1
                    if iPage < num_pages and page_seen[iPage]:
                        initial_squares = most_triggering_list_all_pages[iPage]
                    else:
                        initial_squares = [0] * num_items_per_page

            most_triggering_index_temp = np.array(most_triggering_list_all_pages)
            most_triggering_index = (
                most_triggering_index_temp.flatten()
            )  # vectorizes to single column
            for iItem in range(len(most_triggering_index)):
                if most_triggering_index[iItem] == 1:
                    most_triggering_list.append(unique_sound_labels[iItem])

            # check to make sure enough categories were chosen, if not redo
            if len(most_triggering_list) < num_items_to_select:
                psychopy_present_instructions.function_present_instructions(win, instructions_error, 1)

                done_with_most_triggering = False
                iPage = 0
                page_seen = [False] * num_pages
                most_triggering_list_all_pages = [
                    [0] * num_items_per_page
                ] * num_pages  # initialize index with 0s
                initial_squares = [0] * num_items_per_page  # choices from previous page
                while iPage < num_pages:
                    instructions3 = "Page " + str(iPage + 1) + "/" + str(num_pages)
                    most_triggering_list_page, back_chosen_page = (
                        psychopy_present_item_list.function_present_item_list(
                            unique_sound_labels,
                            num_items_per_page,
                            mean_length,
                            setup_item_height,
                            win,
                            iPage,
                            instructions1,
                            instructions2,
                            "firebrick",
                            instructions3,
                            initial_squares,
                            most_triggering_list,
                            done_with_most_triggering,
                        )
                    )
                    page_seen[iPage] = True
                    most_triggering_list_all_pages[iPage] = most_triggering_list_page

                    if back_chosen_page:  # if participant chooses back button
                        iPage -= 1
                        initial_squares = most_triggering_list_all_pages[iPage]
                    else:
                        iPage += 1
                        if iPage < num_pages and page_seen[iPage]:
                            initial_squares = most_triggering_list_all_pages[iPage]
                        else:
                            initial_squares = [0] * num_items_per_page

                most_triggering_index_temp = np.array(most_triggering_list_all_pages)
                most_triggering_index = (
                    most_triggering_index_temp.flatten()
                )  # vectorizes to single column
                most_triggering_list = []
                for iItem in range(len(most_triggering_index)):
                    if most_triggering_index[iItem] == 1:
                        most_triggering_list.append(unique_sound_labels[iItem])

            done_with_most_triggering = True

    """
    ----------- Refine trigger sounds --------------------------------------------------------
    """
    if (setup_steps.get('step_refine_trigger') is True):
        import psychopy_refine_item_list

        instructions_break1 = (
            "Great! \n\nOn the next page, you will see the sounds you selected. "
            + "\n\nPlease choose your TOP "
            + str(num_items_to_select)
            + " most triggering \nsounds from this list, "
            + "and rank order them from \n1 (more triggering) to "
            + str(num_items_to_select)
            + " (less triggering)."
        )
        instructions4 = (
            "Please rank the \n\nsounds you \nare triggered by. "
            + "\n\n1 = more triggering\n"
            + str(num_items_to_select)
            + " = less triggering \n\n"
            + "Once you have \nselected your top "
            + str(num_items_to_select)
            +", \ncontinue to the \nnext page."
        )
        instructions5 = ("TOP " 
                         + str(num_items_to_select)
                         +"\n\n\n\n\n\n\n\n\n\n")

        psychopy_present_instructions.function_present_instructions(win, instructions_break1, 2)

        refined_most_triggering_list = []
        [most_triggering_list_refined, most_triggering_ranks] = (
            psychopy_refine_item_list.function_present_refined_item_list(
                num_items_to_select,
                mean_length,
                setup_item_height,
                win,
                most_triggering_list,
                instructions4,
                instructions5,
                "firebrick",
            )
        )
        for iItem in range(len(most_triggering_list)):
            if most_triggering_list_refined[iItem] == 1:
                refined_most_triggering_list.append(
                    [most_triggering_ranks[iItem], most_triggering_list[iItem]]
                )

        refined_most_triggering_list = sorted(refined_most_triggering_list)

    """
    ----------- Select neutral sounds --------------------------------------------------------
    """
    if (setup_steps.get('step_select_neutral') is True):
        if (setup_steps.get('step_select_trigger') is False): #if this is the only/first category participants select
            instructions6 = (
                "First, please choose \nthe sounds you \nfind most"
                + "\n\n\n\nIf all of these sounds\nare triggering, \ncontinue to the \nnext page."
            )
            instructions7 = "\nNEUTRAL\n\n\n\n\n"
            done_with_most_triggering = False
            most_triggering_list = []
        else:
            instructions_break2 = (
                "Next, you will repeat this process with sounds "
                + "\nyou find the LEAST triggering or MOST NEUTRAL."
            )
            instructions6 = (
                "Now, please choose \nthe sounds you \nfind most"
                + "\n\n\n\nIf all of these sounds\nare triggering, \ncontinue to the \nnext page."
            )
            instructions7 = "\nNEUTRAL\n\n\n\n\n"

            psychopy_present_instructions.function_present_instructions(win, instructions_break2, 2)

        iPage = 0
        page_seen = [False] * num_pages
        least_triggering_list_all_pages = [
            [0] * num_items_per_page
        ] * num_pages  # initialize index with 0s
        initial_squares = [0] * num_items_per_page  # choices from previous page
        while iPage < num_pages:
            instructions3 = "Page " + str(iPage + 1) + "/" + str(num_pages)
            least_triggering_list_page, back_chosen_page = (
                psychopy_present_item_list.function_present_item_list(
                    unique_sound_labels,
                    num_items_per_page,
                    mean_length,
                    setup_item_height,
                    win,
                    iPage,
                    instructions6,
                    instructions7,
                    "green",
                    instructions3,
                    initial_squares,
                    most_triggering_list,
                    done_with_most_triggering,
                )
            )
            page_seen[iPage] = True
            least_triggering_list_all_pages[iPage] = least_triggering_list_page

            if back_chosen_page:  # if participant chooses back button
                iPage -= 1
                initial_squares = least_triggering_list_all_pages[iPage]
            else:
                iPage += 1
                if iPage < num_pages and page_seen[iPage]:
                    initial_squares = least_triggering_list_all_pages[iPage]
                else:
                    initial_squares = [0] * num_items_per_page

        least_triggering_index_temp = np.array(least_triggering_list_all_pages)
        least_triggering_index = (
            least_triggering_index_temp.flatten()
        )  # vectorizes to single column
        least_triggering_list = []
        for iItem in range(len(least_triggering_index)):
            if least_triggering_index[iItem] == 1:
                least_triggering_list.append(unique_sound_labels[iItem])

        num_available_to_select = num_sound_labels - len(most_triggering_list)

        # check to make sure enough categories were chosen, if not redo 
        if num_available_to_select < num_items_to_select: # if there were less than X options to choose from
            num_items_to_select = num_available_to_select
            
        if (len(least_triggering_list) < num_items_to_select): 
            psychopy_present_instructions.function_present_instructions(win, instructions_error, 1)

            iPage = 0
            page_seen = [False] * num_pages
            least_triggering_list_all_pages = [
                [0] * num_items_per_page
            ] * num_pages  # initialize index with 0s
            initial_squares = [0] * num_items_per_page  # choices from previous page
            while iPage < num_pages:
                instructions3 = "Page " + str(iPage + 1) + "/" + str(num_pages)
                least_triggering_list_page, back_chosen_page = (
                    psychopy_present_item_list.function_present_item_list(
                        unique_sound_labels,
                        num_items_per_page,
                        mean_length,
                        setup_item_height,
                        win,
                        iPage,
                        instructions6,
                        instructions7,
                        "green",
                        instructions3,
                        initial_squares,
                        most_triggering_list,
                        done_with_most_triggering,
                    )
                )
                page_seen[iPage] = True
                least_triggering_list_all_pages[iPage] = least_triggering_list_page

                if back_chosen_page:  # if participant chooses back button
                    iPage -= 1
                    initial_squares = least_triggering_list_all_pages[iPage]
                else:
                    iPage += 1
                    if iPage < num_pages and page_seen[iPage]:
                        initial_squares = least_triggering_list_all_pages[iPage]
                    else:
                        initial_squares = [0] * num_items_per_page

            least_triggering_index_temp = np.array(least_triggering_list_all_pages)
            least_triggering_index = (
                least_triggering_index_temp.flatten()
            )  # vectorizes to single column
            least_triggering_list = []
            for iItem in range(len(least_triggering_index)):
                if least_triggering_index[iItem] == 1:
                    least_triggering_list.append(unique_sound_labels[iItem])

    """
    ----------- Refine neutral sounds --------------------------------------------------------
    """
    if (setup_steps.get('step_refine_neutral') is True):
        if (setup_steps.get('step_refine_trigger') is False): #if haven't seen refinement instructions yet
            import psychopy_refine_item_list
            instructions_break1 = (
                "Great! \n\nOn the next page, you will see the sounds you selected. "
                + "\n\nPlease choose your TOP "
                + str(num_items_to_select)
                + " most neutral \nsounds from this list, "
                + "and rank order them from \n1 (more neutral) to "
                + str(num_items_to_select)
                + " (less neutral)."
            )
            psychopy_present_instructions.function_present_instructions(win, instructions_break1, 2)

        
        instructions8 = (
            "Please rank the \n\nsounds to you. \n\n1 = more neutral\n"
            + str(num_items_to_select)
            + " = less neutral "
            + "\n\n\nOnce you have \nselected your top "
            + str(num_items_to_select)
            + ", \ncontinue to the \nnext page."
        )
        instructions9 = (
            str(num_items_to_select)
            + " MOST NEUTRAL\n\n\n\n\n\n\n\n\n\n"
        )

        refined_least_triggering_list = []
        [least_triggering_list_refined, least_triggering_ranks] = (
            psychopy_refine_item_list.function_present_refined_item_list(
                num_items_to_select,
                mean_length,
                setup_item_height,
                win,
                least_triggering_list,
                instructions8,
                instructions9,
                "green",
            )
        )
        for iItem in range(len(least_triggering_list)):
            if least_triggering_list_refined[iItem] == 1:
                refined_least_triggering_list.append(
                    [least_triggering_ranks[iItem], least_triggering_list[iItem]]
                )

        refined_least_triggering_list = sorted(refined_least_triggering_list)

    instructions_done = "Done!"
    psychopy_present_instructions.function_present_instructions(win, instructions_done, 1)
    win.close()

"""
-------------------------------------------------------------------------------
                        Organize sound selections
-------------------------------------------------------------------------------
"""
if (setup_steps.get('step_organize_sounds') is True):
    with open(file_name, "w") as textfile:
        if (setup_steps.get('step_refine_sound_list') is True):
            print(
                "SOUND_TYPE\t",
                "RANK\t",
                "SOUND_LABEL\t\t",
                "FILE_NAME(S)",
                file=textfile,
            )
        else:
            print("SOUND_TYPE\t", "SOUND_LABEL\t\t", "FILE_NAME(S)", file=textfile)

    # Cycle through selections to grab path names
    if (setup_steps.get('step_select_trigger') is True):
        most_trigger_paths = []
        rank_position = 0
        for iMost in most_triggering_list:
            current_path = all_sound_files[np.char.find(all_sound_labels, iMost) >= 0]
            with open(file_name, "a") as textfile:
                if (setup_steps.get('step_refine_trigger') is True):
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

    if (setup_steps.get('step_select_neutral') is True):
        least_trigger_paths = []
        rank_position = 0
        for iLeast in least_triggering_list:
            current_path = all_sound_files[np.char.find(all_sound_labels, iLeast) >= 0]
            with open(file_name, "a") as textfile:
                if (setup_steps.get('step_refine_neutral') is True):
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
