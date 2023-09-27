from file_io import *
from file_editor import *


def test_config_path_non_existent():
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


def test_read_tds():
    conf_path, config = read_tds("test_tds-server.json")
    assert conf_path == "test_tds-server.json"
    assert config is not None
    assert isinstance(config, dict)
    assert "db" in config
    assert isinstance(config["db"], dict)
    assert "common-file" in config["db"]
    assert (
        config["db"]["common-file"]
        == "C:/ProgramData/tessonics/tds2/data/database.sqlite3"
    )
    assert "measurement-storage" in config["db"]
    assert isinstance(config["db"]["measurement-storage"], dict)
    assert "db-file" in config["db"]["measurement-storage"]
    assert (
        config["db"]["measurement-storage"]["db-file"]
        == "C:/ProgramData/tessonics/tds2/data/measurements.sqlite3"
    )
    assert "backup-bytes" in config["db"]["measurement-storage"]
    assert config["db"]["measurement-storage"]["backup-bytes"] == 1073741824


def test_read_tds_default_location():
    # Requires a tds-server.json in the default location + TDS2 installed
    conf_path, config = read_tds(None)
    assert conf_path == "C:/ProgramData/tessonics/tds2/tds-server.json"
    assert config is not None


def test_read_schema_from_tds():
    # Requires TDS2 installed
    schema = read_schema(None)
    assert "properties" in schema
    assert (
        schema["properties"]["db"]["properties"]["measurement-storage"]["properties"][
            "db-file"
        ]["title"]
        == "Database file"
    )


def test_save_config_no_permission():
    window = tk.Tk()
    try:
        save(
            {"db": {"common-file": tk.StringVar(value="Some Path")}},
            "C:/Windows/no_permission.json",
        )
        assert False
    except PermissionError:
        assert True
