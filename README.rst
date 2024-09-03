.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

.. image:: https://readthedocs.org/projects/misosoupy/badge/?version=latest
    :alt: ReadTheDocs
    :target: https://misosoupy.readthedocs.io/en/stable/
.. image:: https://img.shields.io/coveralls/github/miso-sound/misosoupy/main.svg
    :alt: Coveralls
    :target: https://coveralls.io/r/miso-sound/misosoupy
    .. image:: https://img.shields.io/pypi/v/misosoupy.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/misosoupy/
    .. image:: https://img.shields.io/conda/vn/conda-forge/misosoupy.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/misosoupy
    .. image:: https://pepy.tech/badge/misosoupy/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/misosoupy
|

=========
MisoSOUPy
=========


    Misophonia Stimulus Organization Using Python


A Python package to customize stimuli for experiments on misophonia based on participants' self-reported triggers.


About
=====

Given the individual variability in sounds found to be triggering in misophonia, research experiments benefit from personalizing the stimuli for each participant. For instance, if a participant is bothered by office sounds but not chewing sounds, a study aiming to observe the effects of trigger sounds on performance wouldn't accurately capture the phenomenon if only chewing sounds were used in the experiment. 

MisoSOUPy exists to assist researchers in optimizing their experimental stimuli for each participant via a user-friendly selection process onscreen. Specifically, MisoSOUPy does the following:
   1) imports a list of sounds/stimuli that an experimenter has access to;
   2) displays the names of each sound in alphabetical order for participants to select which ones they find triggering (or not triggering);
   3) allows further refinement of the personalized sounds by requesting participants rank order the sounds they selected; and
   4) outputs a list of all sounds selected and ranked by the participant into a .txt file, including filenames for each sound for easy importation into a separate experimental paradigm.


Examples
========

**In the command window, you will first be prompted to supply the participant number (or press 'Enter' for testing) as well as which sound list to select from, if multiple are found.**

.. figure:: ./docs/media/0_MisoSoupy_DemoVid.gif

*Example: Typing participant "sub01" and selecting "sound_list.csv"*

**Participants then see an instruction screen. Options are customizable, depending on which categories of sounds (and how many stimuli in each) are desired.**

.. figure:: ./docs/media/instructions2.png 

*Example: Instructions for selecting both Trigger and Neutral sounds, at least 5 in each.*

.. figure:: ./docs/media/instructions3.png
   :scale: 50 % 
   :width: 100 px

*Example: Instructions for selecting only Trigger sounds, at least 4.*

**Participants select sounds by clicking the box next to the name.** 

.. figure:: ./docs/media/4_MisoSoupy_DemoVid.gif

*Example: Selecting trigger sounds from the FOAMS sound list*

**For large stimulus sets, multiple pages may exist. Participants may click between pages and change answers as they go.**

.. figure:: ./docs/media/1_MisoSoupy_DemoVid.gif

*Example: Selecting trigger sounds from the NaturalSounds165 sound bank (Norman‐Haignere et al., 2015), utilizing the back button.*

**If fewer sounds than the required number are selected, the participant begins selection again.**

.. figure:: ./docs/media/7_MisoSoupy_DemoVid.gif

*Example: Selecting too few sounds leads to an error screen.*

**Once trigger sounds are selected, participants are presented with their selections and asked to rank order their top choices (corresponding to the number of desired sounds set by the experimenter) by clicking the box next to the name.**

.. figure:: ./docs/media/refinement1.png

*Example: Instructions for refining sound selections, ranking the top 3.*

.. figure:: ./docs/media/5_MisoSoupy_DemoVid.gif

*Example: Ranking trigger sound selections from 1 (more triggering) to 3 (less triggering).*

**When more sounds are selected than need are needed for an experiment, not all sounds will be ranked. Refining the top sounds helps the researcher keep the number of sound choices consistent across participants.** 

.. figure:: ./docs/media/2_MisoSoupy_DemoVid.gif

*Example: Ranking top 5 trigger selections, leaving the rest blank.*

**If neutral sound selections are also desired for the experiment, the process may be repeated with neutral sounds. Participants see the same list again, with their previous (trigger) choices grayed out. They then rank their selections as before.**

.. figure:: ./docs/media/6_MisoSoupy_DemoVid.gif

*Example: Selecting neutral sounds from the remaining items, then ranking top 3.*

**When ranking sounds, choices may be reset and changed if necessary.**

.. figure:: ./docs/media/3_MisoSoupy_DemoVid.gif

*Example: Ranking top 5 neutral sounds, utilizing the reset button to make changes.*

**After selecting and ranking sounds, the participant's choices will be output to a tab-delimited .txt file.**

.. figure:: ./docs/media/data1.png

*Example: Sample output from selection and ranking of FOAMS stimuli.*

.. figure:: ./docs/media/data2.png

*Example: Sample output from selection and ranking of NaturalSounds165 stimuli (Norman‐Haignere et al., 2015).*

.. figure:: ./docs/media/data3.png

*Example: Sample output from selection and ranking of FOAMS stimuli for trigger sounds only.*

.. figure:: ./docs/media/data4.png

*Example: Sample output from selection of FOAMS stimuli for both trigger and neutral sounds, without the ranking step.*


Setup
=====

To use MisoSOUPy, open and run ``run_misosoupy.py`` 

By default, MisoSOUPy will request participants select and rank their top 5 trigger and neutral sounds. To change these default settings, edit ``config.ini``

*Example: change ``step_select_neutral`` to ``False`` in ``config.ini`` to only have participants select triggers sounds.*
   
   # Request participants select their least triggering (or neutral) sounds. If triggering sounds are selected first, these options will remain in the list but appear grayed out. Step_select_sound_list must be True for this option to be True. (Default = True)
   ``step_select_neutral = True``

*Example: change the value for ``num_items_to_select`` in ``config.ini`` to match how many stimuli per category are needed for the experiment.*
   
   # Minimum number of sound labels participants must select in each sound category. If fewer labels than this number are selected, participants see an error screen and must restart. If step_refine_sound_list = True, participants will also rank order this number of sounds. Default = 5.
  ``num_items_to_select = 5``

Put a folder with your sound files (or a .csv of the sound names, see ``FOAMS_sound_list.csv`` for an example) in the ``/misosoupy/assets/`` directory. Sound labels will be derived from the file names (or .csv) in this folder for presentation by MisoSOUPy.


Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd misosoupy
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

.. _pre-commit: https://pre-commit.com/
