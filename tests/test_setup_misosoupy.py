import os
from pathlib import Path

from misosoupy import setup_misosoupy


def test_get_home_dir():
    """
    Tests the functionality of the get_home_dir function.

    Verifies that the returned home directory path exists and is a directory,
    that its name matches the expected 'misosoupy' directory, and that the
    current working directory is the returned home directory.
    """
    home_dir = setup_misosoupy.get_home_dir()
    assert Path(home_dir).is_dir()
    assert Path(home_dir).name == "misosoupy"
    # Not really sure why it is necessary to change the cwd
    # But it is what the function is stated to do
    assert os.getcwd() == home_dir
