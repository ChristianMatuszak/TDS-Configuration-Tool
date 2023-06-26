import tkinter as tk
from file_io import *
from tkinter import messagebox


FRAME_PADDING = 5


def dict_ent(root: dict, root_frame):
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
    messagebox.showinfo("saved", "changes saved")


def restart_button():
    messagebox.showinfo("restart", "service restarted")
