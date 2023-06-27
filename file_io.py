import json
import os
import datetime as dt
from pathlib import Path


def read_tds():
    """read the tds-server.json file

    Returns:
        return: return dict for the json file
    """
    config_file = "tds-server.json"

    with open(config_file, "r") as f:
        return json.loads(f.read())


def read_schema():
    """read the schema.json file

    Returns:
        return: return dict for the json file
    """
    schema_file = "schema.json"

    with open(schema_file, "r") as f:
        return json.loads(f.read())


def save_tds():
    """function to save chaged values in the tds-server file

    work in progress
    """
    tds_file = "tds-server.json"


def path_server():
    """shows the path of the tds-server file

    Returns:
        path: returns the path aof tds-server.json file
    """
    return os.path.abspath("tds-server.json")


def last_modified(config_path: Path):
    """get the last modified time on the tds-server file

    Returns:
        date: returns date and time when the file was last edited
    """
    last_modified = dt.datetime.fromtimestamp(os.path.getmtime(path))

    return last_modified.strftime("%d.%m.%Y  - %H:%M")


def system_running():
    """returns the state of the service Tessonics Mint Node

    Returns:
        text: display the state of Tessonics Mint Node service
    """
    state = os.popen("sc query Tessonics-Mint-Node").read()
    if state.find("RUNNING") != -1:
        return "running"
    else:
        return "stopped"


path = path_server()
