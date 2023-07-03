import tkinter as tk
from file_io import *
from tkinter import messagebox
from tkinter import ttk

FRAME_PADDING = 5


def populate_tabs(schema: dict, root, tds):
    """iterate through the schema.json and for every porperty_key it will create a new Tab

    Args:
        schema (dict): the schema.json file
        root (ttk.Frame): Frame for the Tab windows
        tds (dict): Information from the tds-server.json file

    Returns:
        string: return of the vales for the dict_ent function
    """
    form_tab = {}
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, pady=FRAME_PADDING)

    for property_key, property_schema in schema["properties"].items():
        body_frame = ttk.Frame()
        body_frame.pack(fill="both", expand=True)
        form_tab[property_key] = dict_ent(
            property_schema, body_frame, tds[property_key]
        )
        notebook.add(body_frame, text=property_schema["title"])

    return form_tab


def dict_ent(schema: dict, root_frame, root):
    """creates a frame and entry for all entries in the tds-server.json file

    Args:
        root (dict): the root dict is the tds-server.json file
        root_frame (tk.Frame): Frame to show the read data
    """
    form_state = {}
    for property_key, property_schema in schema["properties"].items():
        if property_schema["type"] == "object":
            frm = ttk.LabelFrame(
                root_frame, text=property_schema["title"], width=10, height=5
            )
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
            tk.Label(entry_frame, text=property_schema["title"], anchor="w").pack(
                expand=1,
                fill=tk.BOTH,
                padx=0,
                pady=5,
                side=tk.LEFT,
            )

            if property_schema["type"] == "string":
                if property_key in root:
                    form_state[property_key] = tk.StringVar(value=root[property_key])
                    ttk.Entry(
                        entry_frame,
                        textvariable=form_state[property_key],
                    ).pack(
                        fill=tk.X,
                        ipadx=110,
                        pady=2,
                        side=tk.LEFT,
                    )
                else:
                    form_state[property_key] = tk.StringVar()
            elif property_schema["type"] == "integer":
                if property_key in root:
                    form_state[property_key] = tk.IntVar(value=root[property_key])
                    ttk.Entry(
                        entry_frame,
                        textvariable=form_state[property_key],
                        validate="key",
                        validatecommand=(root_frame.register(validate_int), "%S"),
                    ).pack(fill=tk.X, ipadx=110, pady=2, side=tk.LEFT)
                else:
                    form_state[property_key] = tk.IntVar(0)
            elif property_schema["type"] == "boolean":
                if property_key in root:
                    form_state[property_key] = tk.BooleanVar(value=root[property_key])
                    ttk.Checkbutton(
                        entry_frame, variable=form_state[property_key]
                    ).pack(fill=tk.X, ipadx=172, pady=2, side=tk.LEFT, anchor="w")
                else:
                    form_state[property_key] = tk.BooleanVar()
    return form_state


def validate_int(new_text):
    """validation to only allow type: int in integer entries.
        it will block any non int type input in the integer entries

    Args:
        new_text (int): checks if the new_text variable is int or not

    Returns:
        _type_: if it is int return True if not retunr False
    """
    if new_text.isnumeric():
        return True
    else:
        return False


def save(form_state: dict):
    """save all changes in the tds-server.json file"""

    def iter_form(parent: dict):
        """function to save changes done by the user

        Args:
            parent (dict): dict where to save the user input (tds-server.json)

        Returns:
            _type_: depends on the data type. These types are: int, str and boolean
        """
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
    """funtion to show the tds-server.json file in the explorer"""
    path = path_server()

    folder = os.path.dirname(path)
    os.startfile(folder)
