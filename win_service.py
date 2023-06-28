import os
from tkinter import messagebox


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
    """returns the state of the service Tessonics Mint Node

    Returns:
        text: display the state of Tessonics Data Server service
    """
    state = os.popen("sc start Tessonics-Data-Service").read()
    if state.find("RUNNING") != -1:
        return messagebox.showinfo("start service", "service started")
    else:
        return messagebox.showerror("ERROR", "service already running")


def stop_service():
    """returns the state of the service Tessonics Mint Node

    Returns:
        text: display the state of Tessonics Data Server service
    """
    state = os.popen("sc stop Tessonics-Data-Service").read()
    return messagebox.showinfo("stop service", "service stoped")
