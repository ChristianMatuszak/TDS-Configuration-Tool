import tkinter as tk
from file_io import *
from tkinter import messagebox

FRAME_PADDING = 5


def dict_ent(root: dict, root_frame):
    """creates a frame and entry for all entries in the tds-server.json file

                        work in progress (name need a change)

    Args:
        root (dict): the root dict is the tds-server.json file
        root_frame (tk.Frame): Frame to show the read data
    """
    for key, value in root.items():
        if isinstance(value, dict):
            frm = tk.Frame(
                root_frame,
                padx=FRAME_PADDING,
                pady=FRAME_PADDING,
                highlightbackground="Grey",
                highlightthickness=2,
            )
            frm.pack(expand=1, fill=tk.BOTH, pady=(0, FRAME_PADDING))
            dict_ent(value, frm)
        else:
            entry_frame = tk.Frame(
                root_frame,
                padx=FRAME_PADDING,
                pady=FRAME_PADDING,
            )
            entry_frame.pack(
                expand=1,
                fill=tk.BOTH,
            )

            input_var = tk.StringVar(value=(value))
            tk.Label(entry_frame, text=key, anchor="w").pack(
                expand=1,
                fill=tk.BOTH,
                padx=0,
                pady=5,
                side=tk.LEFT,
            )
            tk.Entry(
                entry_frame,
                textvariable=input_var,
            ).pack(
                expand=0,
                fill=tk.BOTH,
                ipadx=110,
                pady=2,
                side=tk.LEFT,
            )


def save():
    """save all changes in the tds-server.json file

    work in progress
    """
    messagebox.showinfo("saved", "changes saved")
    save_tds()


def restart():
    """restarts the service

    work in progress
    """
    messagebox.showinfo("restart", "service restarted")


def browse():
    path = path_server()

    folder = os.path.dirname(path)
    os.startfile(folder)


def system_running():
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


def stop_service():
    """returns the state of the service Tessonics Mint Node

    Returns:
        text: display the state of Tessonics Data Server service
    """
    state = os.popen("sc stop Tessonics-Data-Service").read()
