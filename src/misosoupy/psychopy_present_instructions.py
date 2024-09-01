# -*- coding: utf-8 -*-
"""
@author: hhanse
"""

# --- Import packages ---
from psychopy import core, event, visual

# Import config file and screen parameters
import psychopy_exit_out
import setup_misosoupy
[setup_steps, setup_screen]=setup_misosoupy.parse_config_file()

setup_text_color = setup_screen.get('setup_text_color')
setup_screen_color = setup_screen.get('setup_screen_color')
setup_continue_shape_color = setup_screen.get('setup_continue_shape_color')
setup_shape_line_color = setup_screen.get('setup_shape_line_color')

def function_present_instructions(win, instruction_text, wait_time):
        """Present instruction text onscreen using PsychoPy.

        Parameters
        ----------
        instruction_text : str
            Text to display.
        wait_time : int
            Time (in seconds) to pause before CONTINUE button is displayed.
        """

        # Prep instructions
        stim_text_instruction1 = visual.TextStim(
            win,
            text=instruction_text,
            pos=(0, 0),
            color=setup_text_color,
            height=0.09,
            wrapWidth=6,
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
                psychopy_exit_out.function_exit_out(win)

            # Make Continue Button visible after wait_time seconds
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