import tkinter as tk
from tkinter import ttk
from file_editor import *
from file_io import *
from win_service import *

FRAME_PADDING = 5


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent

    def run(self):
        tds = read_tds()

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
            text=path_server(),
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
            text=last_modified(),
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

        canvas = tk.Canvas(frm)
        canvas.pack(side="left", fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        root_frame = tk.Frame(inner_frame)
        root_frame.pack(expand=1, fill=tk.BOTH)

        # function to go through the tds-server.json file
        # and create frames and labels per entry
        self.form_state = dict_ent(read_schema(), root_frame, tds)

        # config to use the mousewheel for scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"),
        )

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_configure)

        show_in_explorer_button = ttk.Button(
            config_path_frame,
            text="show in explorer",
            command=show_in_explorer,
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
            bottom_frame, text="save", command=lambda: save(self.form_state)
        )
        save_button.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.parent.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Editor")
    window.geometry("650x650")
    window.resizable(width=0, height=0)

    window.tk.call("source", "azure.tcl")
    window.tk.call("set_theme", "light")

    style = ttk.Style()
    style.configure("TLabel", backgounrd="Grey")
    style.configure("TLabelframe", background="dodgerblue")

    app = App(window)
    app.pack(fill="both", expand=True)

    app.run()
