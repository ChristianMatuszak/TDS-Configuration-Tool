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
            frm.pack(expand=1, fill=tk.BOTH)
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


def save_button():
    """save all changes in the tds-server.json file

    work in progress
    """
    messagebox.showinfo("saved", "changes saved")
    save_tds()


def restart_button():
    """restarts the service

    work in progress
    """
    messagebox.showinfo("restart", "service restarted")
