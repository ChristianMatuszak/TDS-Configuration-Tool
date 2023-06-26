import tkinter as tk
from file_editor import *
from file_io import *

FRAME_PADDING = 5


def main():
    window = tk.Tk()
    window.title("Editor")
    window.geometry("600x600")
    window.resizable(width=0, height=0)

    # read the tds-server.json file from file-io
    tds = read_tds()

    info_frame = tk.Frame(window)
    info_frame.pack(side=tk.TOP, anchor=tk.W)

    config_path_frame = tk.Frame(info_frame)
    config_path_frame.pack(side=tk.TOP, anchor=tk.W, pady=(0, FRAME_PADDING))

    config_path_label = tk.Label(
        config_path_frame,
        text="config path:",
        padx=9,
        pady=FRAME_PADDING,
        anchor=tk.W,
        highlightbackground="Grey",
        highlightthickness=2,
    )
    config_path_label.pack(side=tk.LEFT)

    config_values_label = tk.Label(
        config_path_frame,
        text=path_server(),
        padx=FRAME_PADDING,
        pady=FRAME_PADDING,
        anchor=tk.W,
    )
    config_values_label.pack(side=tk.LEFT)

    last_modified_frame = tk.Frame(info_frame)
    last_modified_frame.pack(side=tk.TOP, anchor=tk.W, pady=(0, FRAME_PADDING))

    last_modified_label = tk.Label(
        last_modified_frame,
        text="last modified:",
        padx=FRAME_PADDING,
        pady=FRAME_PADDING,
        anchor=tk.W,
        highlightbackground="Grey",
        highlightthickness=2,
    )
    last_modified_label.pack(side=tk.LEFT)

    last_modified_values_label = tk.Label(
        last_modified_frame,
        text=mod_server(),
        padx=FRAME_PADDING,
        pady=FRAME_PADDING,
        anchor=tk.W,
    )
    last_modified_values_label.pack(side=tk.LEFT)

    service_frame = tk.Frame(info_frame)
    service_frame.pack(side=tk.TOP, anchor=tk.W, pady=(0, FRAME_PADDING))

    service_label = tk.Label(
        service_frame,
        text="service:",
        padx=21,
        pady=FRAME_PADDING,
        anchor=tk.W,
        highlightbackground="Grey",
        highlightthickness=2,
    )
    service_label.pack(side=tk.LEFT)

    service_values_label = tk.Label(
        service_frame,
        text=system_running(),
        padx=FRAME_PADDING,
        pady=FRAME_PADDING,
        anchor=tk.W,
    )
    service_values_label.pack(side=tk.LEFT)

    frm = tk.Frame(window)
    frm.pack(expand=True, fill=tk.BOTH)

    canvas = tk.Canvas(frm)
    canvas.pack(side="left", fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frm, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    root_frame = tk.Frame(inner_frame)
    root_frame.pack(expand=1, fill=tk.BOTH)

    # function to go through the tds-server.json file
    # and create frames and labels per entry
    dict_ent(tds, root_frame)

    # config to use the mousewheel for scrolling
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all(
        "<MouseWheel>",
        lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"),
    )

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_configure)

    bottom_frame = tk.Frame(window)
    bottom_frame.pack(side="bottom", fill="both")

    restart = tk.Button(bottom_frame, text="restart", command=restart_button)
    restart.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

    save = tk.Button(bottom_frame, text="save", command=save_button)
    save.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

    window.mainloop()


if __name__ == "__main__":
    main()
