import os
import ctypes, sys
from pathlib import Path
import win32com.shell.shell as shell
import webbrowser
from file_editor import dict_ent


def service_running():
    """returns the state of the service Tessonics Mint Node

    Returns:
        text: display the state of Tessonics Data Server service
    """
    state = os.popen("sc query Tessonics-Data-Service").read()
    if state.find("RUNNING") != -1:
        return True
    else:
        return False


def start_service():
    """returns the state of the service Tessonics Data Server

    Returns:
        text: display the state of Tessonics Data Server service
    """
    shell.ShellExecuteEx(
        lpVerb="runas", lpFile="sc", lpParameters="start Tessonics-Data-Service"
    )


def stop_service():
    """returns the state of the service Tessonics Data Server

    Returns:
        text: display the state of Tessonics Data Server service
    """
    shell.ShellExecuteEx(
        lpVerb="runas", lpFile="sc", lpParameters="stop Tessonics-Data-Service"
    )


def open_browser(configuration):
    url = configuration["server"]["url"] + ":" + str(configuration["server"]["port"])
    webbrowser.open(url, new=0, autoraise=True)
