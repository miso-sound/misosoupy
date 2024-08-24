import pytest

from misosoupy.import_sound_list import function_import_sound_list
from misosoupy.setup_misosoupy import get_path_to_assets


# parametrize
@pytest.mark.parametrize("source", ["sound_list.csv", "naturalsounds165"])
def test_function_import_sound_list(source):
    home_dir = get_path_to_assets()

    results = function_import_sound_list(home_dir, source)

    assert len(results) == 3
