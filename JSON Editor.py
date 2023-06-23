import tkinter as tk
from json import dumps, load


def dict_ent(root: dict, root_frame, canvas):
    for index, (key, value) in enumerate(root.items()):
        if isinstance(value, dict):
            frm = tk.Frame(
                root_frame,
                padx=5,
                pady=5,
            )
            frm.pack(expand=1, fill=tk.BOTH)
            dict_ent(value, frm, canvas)
        else:
            entry_frame = tk.Frame(
                root_frame,
                highlightbackground="Grey",
                highlightthickness=2,
                padx=5,
                pady=5,
            )
            entry_frame.pack(expand=1, fill=tk.BOTH)

            input_var = tk.StringVar(value=dumps(value))
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
window.geometry("600x800")

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

dict_ent(server_config, inner_frame, canvas)

bottom_restart = tk.Frame(window).pack(side="bottom", fill="both", expand=tk.FALSE)
bottom_save = tk.Frame(window).pack(side="bottom", fill="both", expand=tk.FALSE)

restart = tk.Button(bottom_restart, text="restart").pack(
    side=tk.LEFT, expand=1, fill=tk.BOTH
)
save = tk.Button(bottom_save, text="save").pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)


window.mainloop()
