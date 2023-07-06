import tkinter as tk
from tkinter import ttk
from file_editor import *
from file_io import *
from win_service import *
import click


FRAME_PADDING = 5


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent

    def run(self, configuration_path, schema):
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
            text="config path:",
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
            text="last modified:",
            padx=FRAME_PADDING,
            pady=FRAME_PADDING,
            anchor=tk.E,
            width=12,
        )
        last_modified_label.pack(side=tk.LEFT, padx=FRAME_PADDING)

        last_modified_values_label = tk.Label(
            last_modified_frame,
            text=last_modified(configuration_path),
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
            text="service:",
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
            text="show in explorer",
            command=lambda: show_in_explorer(configuration_path),
        )
        show_in_explorer_button.pack(
            side="right", anchor="e", padx=(FRAME_PADDING, FRAME_PADDING)
        )

        start_button = ttk.Button(
            service_frame,
            text="start service",
            command=start_service,
        )
        start_button.pack(side="right", anchor="e", padx=(FRAME_PADDING, FRAME_PADDING))

        stop_button = ttk.Button(
            service_frame, text="stop service", command=stop_service
        )
        stop_button.pack(side="right", anchor="e", padx=FRAME_PADDING)

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(
            side="bottom",
            fill="both",
            padx=(480, 5),
            pady=FRAME_PADDING,
        )

        save_button = ttk.Button(
            bottom_frame,
            text="save",
            command=lambda: save(self.tab_state, configuration_path),
        )
        save_button.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

        # function to go through the schema.json file
        # and create Tabs for every key
        self.tab_state = populate_tabs(read_schema(schema), frm, tds)

        self.parent.mainloop()


@click.command()
@click.option(
    "--configuration",
    help="Path to the tds-server location.",
)
@click.option(
    "--schema",
    help="create the schem.json file if the created file was not found.",
)
def main(configuration, schema):
    window = tk.Tk()
    window.title("Editor")
    window.geometry("700x700")
    window.resizable(width=0, height=0)

    window.tk.call("source", "azure.tcl")
    window.tk.call("set_theme", "light")

    style = ttk.Style()
    style.configure("TLabel", backgounrd="Grey")
    style.configure("TLabelframe", background="dodgerblue")

    app = App(window)
    app.pack(fill="both", expand=True)
    app.run(configuration, schema)


if __name__ == "__main__":
    main()
