import tkinter as tk
from file_io import *
from tkinter import messagebox
from tkinter import ttk

FRAME_PADDING = 5


def dict_ent(schema: dict, root_frame, root):
    """creates a frame and entry for all entries in the tds-server.json file

                        work in progress (name need a change)

    Args:
        root (dict): the root dict is the tds-server.json file
        root_frame (tk.Frame): Frame to show the read data
    """
    form_state = {}
    for property_key, property_schema in schema["properties"].items():
        if property_schema["type"] == "object":
            frm = ttk.LabelFrame(root_frame, text=schema["title"], width=10, height=5)
            frm.pack(
                expand=1, fill=tk.BOTH, pady=(5, FRAME_PADDING), padx=(5, FRAME_PADDING)
            )
            frm.pack(expand=1, fill=tk.BOTH, pady=(0, FRAME_PADDING))
            form_state[property_key] = dict_ent(
                property_schema, frm, root[property_key]
            )
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

            if property_schema["type"] == "string":
                if property_key in root:
                    form_state[property_key] = tk.StringVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.StringVar()
            elif property_schema["type"] == "integer":
                if property_key in root:
                    form_state[property_key] = tk.IntVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.IntVar()
            elif property_schema["type"] == "boolean":
                if property_key in root:
                    form_state[property_key] = tk.BooleanVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.BooleanVar()

            tk.Label(entry_frame, text=property_schema["title"], anchor="w").pack(
                expand=1,
                fill=tk.BOTH,
                padx=0,
                pady=5,
                side=tk.LEFT,
            )
            ttk.Entry(entry_frame, textvariable=form_state[property_key]).pack(
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
