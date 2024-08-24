from misosoupy.import_sound_list import function_import_sound_list
from misosoupy.setup_misosoupy import get_home_dir


def test_function_import_sound_list():
    source = "sound_list.csv"
    home_dir = get_home_dir()

    results = function_import_sound_list(home_dir, source)

    assert len(results) == 3
