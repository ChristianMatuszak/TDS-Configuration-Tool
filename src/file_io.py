import json
import os
import datetime as dt
from tkinter import StringVar
from tkinter.filedialog import askdirectory, askopenfile
from os.path import exists
import subprocess
import sys


def read_tds(configuration_path):
    """read the tds-server.json file

    Returns:
        return: return dict for the json file
    """
    if configuration_path is not None and exists(configuration_path):
        # if not os.path.isfile(configuration_path):
        #    return None, None
        with open(configuration_path, "r") as f:
            return (configuration_path, json.load(f))

    elif configuration_path is None:
        result_path = subprocess.run(
            [
                "C:/Program Files/Tessonics/TDS2/tds-server.exe",
                "show-config",
                "origin",
            ],
            capture_output=True,
        )
        if result_path.returncode == 0:
            configuration_path = result_path.stdout.strip().decode()
            with open(configuration_path, "r") as f:
                return (configuration_path, json.load(f))
    else:
        return None, None


def read_schema(default_schema):
    """read the schema.json file

    Returns:
        return: return dict for the json file
    """
    # 1. Load from command line
    if default_schema is not None:
        return json.loads(default_schema)

    # 2. Load from TDS Application
    else:
        result = subprocess.run(
            ["C:/Program Files/Tessonics/TDS2/tds-server.exe", "show-config", "schema"],
            capture_output=True,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)


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


def open_explorer(entry: StringVar, viewer_type):
    """function to select new path for files and directories

    Args:
        entry (StringVar): current path
        viewer_type (_type_): check if it is a file if not it has to be a directory
    """
    if viewer_type == "text-edit-browse-file":
        parent_directory = os.path.dirname(entry.get())
        new_file = askopenfile(initialdir=parent_directory)
        if new_file is not None:
            entry.set(new_file.name)
    else:
        parent_directory = os.path.dirname(entry.get())
        new_directory = askdirectory(initialdir=parent_directory)
        if new_directory != "":
            entry.set(new_directory)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def tds_version():
    """this function get the current version from TDS

    Returns:
        String: returns the current version as string
    """
    result = subprocess.run(
        ["C:/Program Files/Tessonics/TDS2/tds-server.exe", "version"],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    output_lines = result.stdout.strip().split("\n")
    for line in output_lines:
        if line.strip().startswith("version"):
            version = line.strip().split(":")[1].strip()
    return version
