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
    form_state = {}
    for key, value in root.items():
        if isinstance(value, dict):
            frm = ttk.LabelFrame(root_frame, text=key, width=10, height=5)
            frm.pack(
                expand=1, fill=tk.BOTH, pady=(5, FRAME_PADDING), padx=(5, FRAME_PADDING)
            )
            frm.pack(expand=1, fill=tk.BOTH, pady=(0, FRAME_PADDING))
            form_state[key] = dict_ent(value, frm)
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

            form_state[key] = tk.StringVar(value=(value))
            tk.Label(entry_frame, text=key, anchor="w").pack(
                expand=1,
                fill=tk.BOTH,
                padx=0,
                pady=5,
                side=tk.LEFT,
            )
            ttk.Entry(
                entry_frame,
                textvariable=form_state[key],
            ).pack(
                expand=0,
                fill=tk.BOTH,
                ipadx=110,
                pady=2,
                side=tk.LEFT,
            )

    return form_state


def save(form_state: dict):
    """save all changes in the tds-server.json file

    work in progress
    """

    def iter_form(parent: dict):
        state = {}
        for key, value in parent.items():
            if isinstance(value, dict):
                state[key] = iter_form(parent[key])
            else:
                state[key] = value.get()
        return state

    result = iter_form(form_state)

    messagebox.showinfo("saved", "changes saved")
    save_tds(result)


def show_in_explorer():
    path = path_server()

    folder = os.path.dirname(path)
    os.startfile(folder)
