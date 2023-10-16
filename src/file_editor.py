import tkinter as tk
from file_io import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import askyesno
import webbrowser
from idlelib.tooltip import Hovertip

FRAME_PADDING = 5


def populate_tabs(schema: dict, root, tds):
    """iterate through the schema.json and for every porperty_key it will
        create a new Tab

    Args:
        schema (dict): the schema.json file
        root (ttk.Frame): Frame for the Tab windows
        tds (dict): Information from the tds-server.json file

    Returns:
        string: returns a dict of all state variables of the tabs form
    """
    tab_form_state = {}
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, pady=FRAME_PADDING)

    for property_key, property_schema in schema["properties"].items():
        body_frame = ttk.Frame()
        body_frame.pack(fill="both", expand=True)

        tab_form_state[property_key] = populate_tab_form(
            property_schema, body_frame, tds[property_key] if tds is not None else None
        )
        notebook.add(body_frame, text=property_schema["title"])

    return tab_form_state


def populate_tab_form(schema: dict, root_frame, root):
    """Iterates through the schema.json
        and creates labels and entries for each
        dict and differentiates between the data types

    Args:
        schema (dict): The file that is being iterated
        root_frame (tk.Frame): Frame to show the read data
        root (dict): the root dict is the tds-server.json file

    Returns:
        dict: form with entries
    """
    form_state = {}
    # When it hits another dictionary,
    # it calls the same function on the dictionary too.
    for property_key, property_schema in schema["properties"].items():
        if property_schema["type"] == "object":
            frm = ttk.LabelFrame(
                root_frame, text=property_schema["title"], width=10, height=5
            )
            frm.pack(
                expand=1, fill=tk.BOTH, pady=(5, FRAME_PADDING), padx=(5, FRAME_PADDING)
            )
            frm.pack(expand=1, fill=tk.BOTH, pady=(0, FRAME_PADDING))
            form_state[property_key] = populate_tab_form(
                property_schema, frm, root[property_key] if root is not None else None
            )

        else:
            entry_frame = tk.Frame(root_frame, padx=FRAME_PADDING, pady=FRAME_PADDING)
            entry_frame.pack(expand=1, fill=tk.BOTH)
            label = tk.Label(entry_frame, text=property_schema["title"], anchor="w")
            label.pack(padx=FRAME_PADDING, pady=FRAME_PADDING, side=tk.LEFT)

            # Help icon if a description is available

            if "description" in property_schema:
                info = tk.Label(entry_frame, text="🛈", anchor="w")
                info.pack(side="left")
                Hovertip(info, property_schema["description"])

            seperator_label = tk.Label(entry_frame, anchor="w")
            seperator_label.pack(expand=1, side="left", fill=tk.BOTH)

            # Data type verification (string, integer, boolean)
            # and strings additionally according to file pathsand normal strings
            if property_schema["type"] == "string":
                if root is not None and property_key in root:
                    form_state[property_key] = tk.StringVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.StringVar()

                if "viewer" in property_schema:
                    if (
                        property_schema["viewer"] == "text-edit-browse-file"
                        or "text-edit-browse-dir"
                    ):
                        ttk.Entry(
                            entry_frame,
                            textvariable=form_state[property_key],
                            state="readonly",
                        )
                        ttk.Entry.pack(fill=tk.X, ipadx=110, pady=2, side=tk.LEFT)
                        ttk.Button(
                            entry_frame,
                            text="🗁",
                            width=3,
                            command=lambda viewer_type=property_schema[
                                "viewer"
                            ], path=form_state[property_key]: open_explorer(
                                path, viewer_type
                            ),
                        )
                        ttk.Button.pack(padx=FRAME_PADDING, pady=2, side=tk.RIGHT)
                else:
                    ttk.Entry(entry_frame, textvariable=form_state[property_key])
                    ttk.Entry.pack(fill=tk.X, ipadx=110, pady=2, side=tk.LEFT)

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
                )
                ttk.Entry.pack(fill=tk.X, ipadx=110, pady=2, side=tk.LEFT)

            elif property_schema["type"] == "boolean":
                if root is not None and property_key in root:
                    form_state[property_key] = tk.BooleanVar(value=root[property_key])
                else:
                    form_state[property_key] = tk.BooleanVar()
                ttk.Checkbutton(entry_frame, variable=form_state[property_key])
                ttk.Checkbutton.pack(
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


def save(form_state: dict, configuration_file):
    """Recursive function.
        When it hits another dictionary,
        it calls the same function on the dictionary too.

    Args:
        form_state (dict): with form entries that should be saved
        configuration_file (string): save location

    Returns:
        dict: Dict with form entries
    """

    if configuration_file is None:
        configuration_file = "C:\\ProgramData\\tessonics\\tds2\\tds-server.json"

    def iter_form(parent: dict):
        """function to create the new dict that should be saved

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


def save_handler(tab_state, configuration_path, window):
    """function to give the save function the exit_program = True argument
    after pressing the save_and_exit button

    Args:
        tab_state (dict): the dict with all changes from the entries
        configuration_path (str): The path of the tds-server .json file to save the changes
        window (ttk.Frame): Frame that will be closed after pressing the button
    """
    try:
        save(
            tab_state,
            configuration_path,
        )
        messagebox.showinfo("Saved", "Changes have been successfully saved.")
    except PermissionError:
        messagebox.showerror(
            "Error", " Permission denied. \n Please restart programm as admin!"
        )


def confirm_handler(window):
    """Window with a yes and no button if the application
        should be closed or remain open after pressing the X button

    Args:
        window (tk.Frame): Window with a yes and no button
    """
    answer = askyesno(
        title="Close Configuration-Tool",
        message="close application? \n\n Unsaved changes will be lost!",
    )

    if answer:
        window.destroy()
    else:
        window.attributes("-disabled", False)


def open_help():
    """function that opens the installation guide in the webbrowser"""
    url = "https://tessonics.github.io/user-docs/v4/installation-guide/fulltext.html"
    webbrowser.open(url, new=0, autoraise=True)
