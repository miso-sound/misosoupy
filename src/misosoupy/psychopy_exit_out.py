# -*- coding: utf-8 -*-
"""
@author: hhanse
"""

# --- Import packages ---
from psychopy import core, logging

def function_exit_out(win):
    """Safely exit out of presentation, closing window and flushing log."""

    logging.flush()
    win.close()
    core.quit()