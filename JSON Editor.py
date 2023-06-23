import tkinter as tk
from json import dumps, load
import os

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


def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


with open("tds-server.json") as file:
    server_config = load(file)

window = tk.Tk()
window.title("Editor")
window.geometry("600x600")

info_frame = tk.Frame(window).pack(side=tk.TOP)
patch_frame = tk.Frame(info_frame).pack(expand=0, fill=tk.BOTH)
path = tk.Label(
    info_frame,
    text="Config Path",
    padx=FRAME_PADDING,
    pady=FRAME_PADDING,
    highlightbackground="Grey",
    highlightthickness=2,
).pack()
path_label = tk.Label(
    info_frame,
    text="values",
    padx=FRAME_PADDING,
    pady=FRAME_PADDING,
    highlightbackground="Grey",
    highlightthickness=2,
).pack()
mod_frame = tk.Frame(info_frame).pack(expand=0, fill=tk.BOTH)
mod = tk.Label(
    info_frame,
    text="last modified",
    padx=FRAME_PADDING,
    pady=FRAME_PADDING,
    highlightbackground="Grey",
    highlightthickness=2,
).pack()
mod_label = tk.Label(
    info_frame,
    text="values",
    padx=FRAME_PADDING,
    pady=FRAME_PADDING,
    highlightbackground="Grey",
    highlightthickness=2,
).pack()
service_frame = tk.Frame(info_frame).pack(expand=0, fill=tk.BOTH)
service = tk.Label(
    info_frame,
    text="service running/stopped",
    padx=FRAME_PADDING,
    pady=FRAME_PADDING,
    highlightbackground="Grey",
    highlightthickness=2,
).pack()
service_label = tk.Label(
    info_frame,
    text="values",
    padx=FRAME_PADDING,
    pady=FRAME_PADDING,
    highlightbackground="Grey",
    highlightthickness=2,
).pack()

frm = tk.Frame(window)
frm.pack(expand=True, fill=tk.BOTH)

canvas = tk.Canvas(frm)
canvas.pack(side="left", fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frm, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", on_canvas_configure)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

dict_ent(server_config, inner_frame)

bottom_restart = tk.Frame(window).pack(side="bottom", fill="both", expand=tk.FALSE)
bottom_save = tk.Frame(window).pack(side="bottom", fill="both", expand=tk.FALSE)

restart = tk.Button(bottom_restart, text="restart").pack(
    side=tk.LEFT, expand=1, fill=tk.BOTH
)
save = tk.Button(bottom_save, text="save").pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)

window.mainloop()
