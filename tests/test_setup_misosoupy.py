from pathlib import Path

from misosoupy.setup_misosoupy import get_path_to_assets

def test_get_path_to_assets():
    result = get_path_to_assets()

    assert isinstance(result, Path)
    assert result.is_dir()
    assert result.name == "assets"
