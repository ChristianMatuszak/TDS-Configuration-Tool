import tkinter as tk
from file_io import *
from tkinter import messagebox
from tkinter import ttk
import sys

FRAME_PADDING = 5


def populate_tabs(schema: dict, root, tds):
    """iterate through the schema.json and for every porperty_key it will create a new Tab

    Args:
        schema (dict): the schema.json file
        root (ttk.Frame): Frame for the Tab windows
        tds (dict): Information from the tds-server.json file

    Returns:
        string: returns a dict of all state variables of the tabs form
    """
    form_tab = {}
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, pady=FRAME_PADDING)

    for property_key, property_schema in schema["properties"].items():
        body_frame = ttk.Frame()
        body_frame.pack(fill="both", expand=True)

        form_tab[property_key] = dict_ent(
            property_schema, body_frame, tds[property_key] if tds is not None else None
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
                property_schema, frm, root[property_key] if root is not None else None
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
                if root is not None and property_key in root:
                    form_state[property_key] = tk.StringVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.StringVar()
                ttk.Entry(
                    entry_frame,
                    textvariable=form_state[property_key],
                ).pack(
                    fill=tk.X,
                    ipadx=110,
                    pady=2,
                    side=tk.LEFT,
                )
            elif property_schema["type"] == "integer":
                if root is not None and property_key in root:
                    form_state[property_key] = tk.IntVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.IntVar(value=0)
                ttk.Entry(
                    entry_frame,
                    textvariable=form_state[property_key],
                    validate="key",
                    validatecommand=(root_frame.register(validate_int), "%S"),
                ).pack(fill=tk.X, ipadx=110, pady=2, side=tk.LEFT)
            elif property_schema["type"] == "boolean":
                if root is not None and property_key in root:
                    form_state[property_key] = tk.BooleanVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.BooleanVar()
                ttk.Checkbutton(entry_frame, variable=form_state[property_key]).pack(
                    fill=tk.X, ipadx=172, pady=2, side=tk.LEFT, anchor="w"
                )
    return form_state


def validate_int(new_text):
    """validation to only allow type: int in integer entries.
        it will block any non int type input in the integer entries

    Args:
        new_text (str): It contains the most rescent added text

    Returns:
        boolean: if it is int return True if not return False
    """
    if new_text.isnumeric():
        return True
    else:
        return False


def save(form_state: dict, configuration_file, exit_program=False):
    """save all changes in the tds-server.json file"""

    if configuration_file is None:
        configuration_file = "C:\\ProgramData\\tessonics\\tds2\\tds-server.json"

    def iter_form(parent: dict):
        """function to save changes done by the user

        Args:
            parent (dict): dict where to save the user input (tds-server.json)

        Returns:
            dict: returns the current data contents of all forms
        """
        state = {}
        for key, value in parent.items():
            if isinstance(value, dict):
                state[key] = iter_form(parent[key])
            else:
                state[key] = value.get()
        return state

    result = iter_form(form_state)

    save_tds(result, configuration_file)
    messagebox.showinfo("saved", "changes saved")
    if exit_program:
        sys.exit()


def save_button_handler(tab_state, configuration_path):
    """function to give the save function the exit_program = False argmunet
    after pressing the save button

    Args:
        tab_state (dict): the dict with all changes from the entries
        configuration_path (str): The path of the tds-server .json file to save the changes
    """
    save(tab_state, configuration_path, exit_program=False)


def save_and_exit_handler(tab_state, configuration_path, window):
    """function to give the save function the exit_program = True argument
    after pressing the save_and_exit button

    Args:
        tab_state (dict): the dict with all changes from the entries
        configuration_path (str): The path of the tds-server .json file to save the changes
        window (ttk.Frame): Frame that will be closed after pressing the button
    """
    save(tab_state, configuration_path, exit_program=True)


def confirm_no(confirm_window, window):
    """function not to close the confirm_window after pressing the no button

    Args:
        confirm_window (ttk.Frame): frame with the 3 buttons if you want to close the application
    """
    confirm_window.destroy()
    window.attributes("-disabled", False)


def confirm_yes(confirm_window, window):
    """function to close the confirm_window after pressing the yes button

    Args:
        confirm_window (ttk.Frame): frame with the 3 buttons if you want to close the application_
        window (ttk.Frame): Frame of the main application
    """
    confirm_window.destroy()
    window.destroy()
