import pathlib

import pytest

from example_project_with_rye.util.settings import load_env_settings

BASE_PATH = pathlib.Path(__file__).parent.parent.resolve()
def test_load_settings_with_default_env_file():

    settings = load_env_settings(BASE_PATH/'.env')
    assert settings

def test_load_settings_with_missing_env_file():

    with pytest.raises(ValueError):
        settings = load_env_settings(BASE_PATH/'nonexistant.file')
        assert settings
