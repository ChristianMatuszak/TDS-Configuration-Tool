import tkinter as tk
from tkinter import ttk
from file_editor import *
from file_io import *
from win_service import *
import click
from version import VERSION

FRAME_PADDING = 5


class App(ttk.Frame):
    def __init__(self, parent, configuration_path, schema, window):
        ttk.Frame.__init__(self)
        self.parent = parent

        configuration_path, tds = read_tds(configuration_path)

        info_frame = ttk.LabelFrame(self, text="File Info")
        info_frame.pack(side=tk.TOP, anchor=tk.CENTER)

        config_path_frame = ttk.Frame(info_frame)
        config_path_frame.pack(
            side=tk.TOP,
            fill="both",
            anchor=tk.W,
            pady=(0, FRAME_PADDING),
            padx=FRAME_PADDING,
        )

        config_path_label = tk.Label(
            config_path_frame,
            text="Config Path:",
            padx=FRAME_PADDING,
            pady=FRAME_PADDING,
            anchor=tk.E,
            width=12,
        )
        config_path_label.pack(side=tk.LEFT, padx=FRAME_PADDING)

        config_values_label = tk.Label(
            config_path_frame,
            text=configuration_path,
            padx=FRAME_PADDING,
            pady=FRAME_PADDING,
            anchor=tk.W,
        )
        config_values_label.pack(side=tk.LEFT, expand=1, fill="both")

        last_modified_frame = ttk.Frame(info_frame)
        last_modified_frame.pack(
            side=tk.TOP, anchor=tk.W, pady=(0, FRAME_PADDING), padx=5
        )

        last_modified_label = tk.Label(
            last_modified_frame,
            text="Last Modified:",
            padx=FRAME_PADDING,
            pady=FRAME_PADDING,
            anchor=tk.E,
            width=12,
        )
        last_modified_label.pack(side=tk.LEFT, padx=FRAME_PADDING)

        last_modified_values_label = tk.Label(
            last_modified_frame,
            text=last_modified(configuration_path)
            if configuration_path is not None
            else "not loaded",
            padx=FRAME_PADDING,
            pady=FRAME_PADDING,
            anchor=tk.W,
        )
        last_modified_values_label.pack(side=tk.LEFT)

        service_frame = ttk.Frame(info_frame)
        service_frame.pack(
            expand=1,
            side=tk.TOP,
            fill="both",
            anchor=tk.W,
            pady=(0, FRAME_PADDING),
            padx=FRAME_PADDING,
        )

        service_label = tk.Label(
            service_frame,
            text="Service:",
            padx=FRAME_PADDING,
            pady=FRAME_PADDING,
            anchor=tk.E,
            width=12,
        )
        service_label.pack(side=tk.LEFT, padx=FRAME_PADDING)

        service_values_label = tk.Label(
            service_frame,
            padx=FRAME_PADDING,
            pady=FRAME_PADDING,
            anchor=tk.W,
        )
        service_values_label.pack(side=tk.LEFT)

        def poll_service(window: tk.Tk, value_label: tk.Label):
            if service_running():
                value_label.config(text="Running", anchor="e")
            else:
                value_label.config(text="Stopped", anchor="e")
            window.after(1000, poll_service, window, value_label)

        poll_service(self, service_values_label)

        frm = tk.Frame(self)
        frm.pack(expand=True, fill=tk.BOTH)

        show_in_explorer_button = ttk.Button(
            config_path_frame,
            text="Show in Explorer",
            command=lambda: show_in_explorer(configuration_path),
        )
        show_in_explorer_button.pack(
            side="right", anchor="e", padx=(FRAME_PADDING, FRAME_PADDING)
        )

        start_button = ttk.Button(
            service_frame,
            text="Start Service",
            command=start_service,
        )
        start_button.pack(side="right", anchor="e", padx=(FRAME_PADDING, FRAME_PADDING))

        stop_button = ttk.Button(
            service_frame, text="Stop Service", command=stop_service
        )
        stop_button.pack(side="right", anchor="e", padx=FRAME_PADDING)

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(
            side="bottom",
            fill="both",
            padx=(5, 5),
            pady=FRAME_PADDING,
        )

        help_button = ttk.Button(bottom_frame, text="Help", width=1, command=open_help)
        help_button.pack(side=tk.LEFT, expand=1, fill="both", padx=FRAME_PADDING)

        version_number = ttk.Label(bottom_frame, text=f"Version: {VERSION}")
        version_number.pack(side=tk.LEFT, fill="x", pady=FRAME_PADDING)

        save_button = ttk.Button(
            bottom_frame,
            text="Save",
            command=lambda: save_button_handler(self.tab_state, configuration_path),
        )
        save_button.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, padx=(400, 5))

        def close_app():
            """Function to prevent accidental closure and query whether you are sure with yes, no and save and exit buttons"""
            window.attributes("-disabled", True)

            confirm_window = tk.Toplevel(parent)
            confirm_window.title("Exit")
            confirm_window.geometry("320x150")
            confirm_window.resizable(False, False)
            confirm_window.configure(
                highlightbackground="dodgerblue", highlightthickness=1
            )

            confirm_window.update_idletasks()
            width = confirm_window.winfo_width()
            height = confirm_window.winfo_height()
            x = (window.winfo_width() // 2) - (width // 2) + window.winfo_x()
            y = (window.winfo_height() // 2) - (height // 2) + window.winfo_y()
            confirm_window.geometry(f"+{x}+{y}")
            confirm_window.resizable(False, False)

            confirm_window.overrideredirect(True)

            closing_frame = ttk.Frame(confirm_window)
            closing_frame.pack(side="top", expand=True, fill="both")

            closing_label = ttk.Label(
                closing_frame, text="close application? unsaved changes will be lost"
            )
            closing_label.pack()

            yes_button = ttk.Button(
                confirm_window,
                text="Yes",
                command=lambda: confirm_yes(confirm_window, parent),
            )
            yes_button.pack(side=tk.LEFT, padx=FRAME_PADDING, pady=FRAME_PADDING)
            no_button = ttk.Button(
                confirm_window,
                text="No",
                command=lambda: confirm_no(confirm_window, window),
            )
            no_button.pack(side=tk.LEFT, padx=FRAME_PADDING, pady=FRAME_PADDING)
            save_and_exit_button = ttk.Button(
                confirm_window,
                text="Save and Exit",
                command=lambda: save_and_exit_handler(
                    self.tab_state, configuration_path, parent
                ),
            )
            save_and_exit_button.pack(
                side=tk.LEFT, padx=FRAME_PADDING, pady=FRAME_PADDING
            )

        # function to go through the schema.json file
        # and create Tabs for every key
        self.tab_state = populate_tabs(read_schema(schema), frm, tds)
        parent.protocol("WM_DELETE_WINDOW", close_app)

    def quit_application(self):
        self.window.destroy()

    def run(self):
        try:
            self.parent.mainloop()
        except Exception as e:
            messagebox.showerror("Exception", f"{e}")


@click.command()
@click.option(
    "--configuration",
    help="Path to the tds-server location.",
)
@click.option(
    "--schema",
    help="create the schema.json file if the created file was not found.",
)
def main(configuration, schema):
    window = tk.Tk()
    window.title("Serverkonfiguration")
    window.geometry("700x700")
    window.resizable(width=0, height=0)

    window.tk.call("source", "azure.tcl")
    window.tk.call("set_theme", "light")

    style = ttk.Style()
    style.configure("TLabel", backgounrd="Grey")
    style.configure("TLabelframe", background="dodgerblue")

    app = App(window, configuration, schema, window)
    app.pack(fill="both", expand=True)
    app.run()


if __name__ == "__main__":
    main()
