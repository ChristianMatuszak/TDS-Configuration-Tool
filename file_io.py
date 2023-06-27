import tkinter as tk
import json
import os
import time
import psutil
from pathlib import Path


def read_tds():
    """read the tds-server.json file

    Returns:
        return: return dict for the json file
    """
    file = "tds-server.json"

    with open(file, "r") as f:
        tds = json.loads(f.read())

    return tds


def read_schema():
    """read the schema.json file

    Returns:
        return: return dict for the json file
    """
    file = "schema.json"

    with open(file, "r") as f:
        schema = json.loads(f.read())

    return schema


def save_tds():
    """function to save chaged values in the tds-server file

    work in progress
    """
    file1 = "tds-server.json"


def path_server():
    """shows the path of the tds-server file

    Returns:
        path: location of the tds-server json file
    """
    p = Path.cwd()

    return p


def mod_server():
    """get the last modified time on the tds-server file

    Returns:
        date: returns date and time when the file was last edited
    """
    m1 = os.path.getmtime(path)

    m_ti = time.ctime(m1)

    return m_ti


def system_running():
    """function to check if tds-server is running or not

    Returns:
        text: if it's running return:'running' if not return: 'stopped'

                work in progress(Firefox for testing purposes)

    """
    for proc in psutil.process_iter():
        if "Firefox.exe".lower() in proc.name().lower():
            return "running"
    return "stopped"


path = path_server()
