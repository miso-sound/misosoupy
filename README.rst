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


Setup
=====

To use MisoSOUPy, open and run

   run_misosoupy.py 

In the command window, you will be prompted to supply the participant number (or press 'Enter' for testing) as well as which sound list to select from, if multiple are found.




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
