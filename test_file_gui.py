from file_io import *


def test_dummy():
    assert 1 == 1


def test_config_path():
    config_path_result, config_result = read_tds("does not exist")
    assert config_path_result is None
    assert config_result is None
