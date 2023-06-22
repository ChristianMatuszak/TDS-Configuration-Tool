from tkinter import *
import tkinter as tk
from json import dumps, load
from tkinter import ttk


def dict_ent(root: dict, root_frame):
    for index, (key, value) in enumerate(root.items()):
        if isinstance(value, dict):
            frm = tk.Frame(
                root_frame,
                padx=5,
                pady=5,
            )
            frm.pack(expand=1, fill=BOTH)
            dict_ent(value, frm)
        else:
            entry_frame = tk.Frame(
                root_frame,
                highlightbackground="Grey",
                highlightthickness=2,
                padx=5,
                pady=5,
            )
            entry_frame.pack(expand=1, fill=BOTH)

            input_var = StringVar(value=dumps(value))
            L1 = Label(entry_frame, text=key, anchor="w").pack(
                expand=1,
                fill=BOTH,
                padx=0,
                pady=5,
                side=LEFT,
            )
            E1 = Entry(
                entry_frame,
                textvariable=input_var,
            ).pack(
                expand=0,
                fill=BOTH,
                ipadx=110,
                pady=2,
                side=LEFT,
            )


with open("tds-server.json") as file:
    server_config = load(file)

window = tk.Tk()
window.title("Editor")
window.geometry("1024x800")

frm = tk.Frame(
    window,
)

frm.pack(expand=1, fill=BOTH)

dict_ent(server_config, frm)

window.mainloop()
