import tkinter as tk
from file_io import *
from tkinter import messagebox
from tkinter import ttk

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
            frm = ttk.LabelFrame(root_frame, text=key, width=10, height=5)
            frm.pack(
                expand=1, fill=tk.BOTH, pady=(5, FRAME_PADDING), padx=(5, FRAME_PADDING)
            )
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

            input_var = tk.StringVar(value=value)
            tk.Label(entry_frame, text=f"{key} :", anchor="w").pack(
                expand=1,
                fill=tk.BOTH,
                padx=0,
                pady=5,
                side=tk.LEFT,
            )
            entry = ttk.Entry(
                entry_frame,
            )
            entry.insert(0, value)
            entry.pack(
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


def show_in_explorer():
    path = path_server()

    folder = os.path.dirname(path)
    os.startfile(folder)
