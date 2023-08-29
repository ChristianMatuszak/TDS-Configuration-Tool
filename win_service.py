import os
import ctypes, sys
from pathlib import Path
import win32com.shell.shell as shell


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


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
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
