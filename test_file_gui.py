from file_io import *
from file_editor import *


def test_dummy():
    assert 1 == 1


def test_config_path():
    config_path_result, config_result = read_tds("does not exist")
    assert config_path_result is None
    assert config_result is None


def test_check_nummeric1():
    result = validate_int("12345")
    assert result == True


def test_check_nummeric2():
    result = validate_int("abc")
    assert result == False


def test_check_nummeric3():
    result = validate_int("")
    assert result == False


def test_check_nummeric4():
    result = validate_int("   ")
    assert result == False
