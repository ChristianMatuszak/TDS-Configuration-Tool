import json
import os
import datetime as dt


def read_tds(configuration_path):
    """read the tds-server.json file

    Returns:
        return: return dict for the json file
    """
    if configuration_path is None:
        configuration_path = "tds-server.json"

    with open(configuration_path, "r") as f:
        return (configuration_path, json.load(f))


def read_schema(default_schema):
    """read the schema.json file

    Returns:
        return: return dict for the json file
    """
    if default_schema is not None:
        return json.loads(default_schema)

    with open("schema.json", "r") as f:
        return json.load(f)


def save_tds(config, configuration_path):
    """function to save chaged values in the tds-server file"""

    with open(configuration_path, "w") as f:
        json.dump(config, f, indent=4)


def last_modified(configuration_path):
    """get the last modified time on the tds-server file

    Returns:
        date: returns date and time when the file was last edited
    """
    last_modified = dt.datetime.fromtimestamp(os.path.getmtime(configuration_path))

    return last_modified.strftime("%d.%m.%Y - %H:%M")


def show_in_explorer(configuration_path):
    """funtion to show the tds-server.json file in the explorer"""

    folder = os.path.dirname(configuration_path)
    os.startfile(folder)
