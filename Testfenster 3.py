from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from json import dump, dumps, load, loads
from tkinter import ttk


with open("tds-server.json") as file:

    server_config = load(file)

window = tk.Tk()
window.title("Tab window")
window.maxsize(1280, 720)
window.config(bg="honeydew4")
var = IntVar()
tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text="db")
tabControl.add(tab2, text="server")
tabControl.add(tab3, text="ssl")
tabControl.add(tab4, text='csv')
tabControl.add(tab5, text="branding")
tabControl.pack(expand=1, fill="both")

ttk.Label(tab1, text=dumps(server_config['db'], indent=4)).grid(column=0, row=0, padx=5, pady=5)
ttk.Label(tab2, text=dumps(server_config['server'], indent=4)).grid(column=0, row=0, padx=5, pady=5)
ttk.Label(tab3, text=dumps(server_config['ssl'], indent=4)).grid(column=0, row=0, padx=5, pady=5)
ttk.Label(tab4, text=dumps(server_config['csv'], indent=4)).grid(column=0, row=0, padx=5, pady=5)
ttk.Label(tab5, text=dumps(server_config['branding'], indent=4)).grid(column=0, row=0, padx=5, pady=5)

label = Label(window)
window.mainloop()

