import os
from pathlib import Path

from misosoupy.setup_misosoupy import get_home_dir, get_path_to_assets


def test_get_path_to_assets():
    result = get_path_to_assets()

    assert isinstance(result, Path)
    assert result.is_dir()
    assert result.name == "assets"


def test_get_home_dir():
    """
    Tests the functionality of the get_home_dir function.

    Verifies that the returned home directory path exists and is a directory,
    that its name matches the expected 'misosoupy' directory, and that the
    current working directory is the returned home directory.
    """
    home_dir = get_home_dir()

    assert Path(home_dir).is_dir()
    assert Path(home_dir).name == "misosoupy"
    # Not really sure why it is necessary to change the cwd
    # But it is what the function is stated to do
    assert os.getcwd() == home_dir
