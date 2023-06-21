from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


window = tk.Tk()
window.title("Testfenster 2")
window.maxsize(900, 600)
window.config(bg="honeydew3")
var = IntVar()

left_frame = Frame(window, width=200, height=400, bg="honeydew4")
left_frame.grid(column=0, row=0, padx=10, pady=5)

right_frame = Frame(window, width=650, height=400, bg="honeydew4")
right_frame.grid(column=1, row=0, padx=10, pady=5)

Label(left_frame, text="Standard").grid(column=0, row=0, padx=5, pady=5)

image = PhotoImage(file="Beispiel.png")
original_image = image.subsample(3,3)
Label(left_frame, image=original_image).grid(column=0, row=1, padx=5, pady=5)

Label(right_frame, image=image).grid(column=0, row=0, padx=5, pady=5)

tool_bar = Frame (left_frame, width=180, height=185)
tool_bar.grid(column=0, row=2, padx=5, pady=5)

Label(tool_bar, text="Bezeichnung", relief=RAISED).grid(column=0, row=0, padx=5, pady=3, ipadx=10)
Label(tool_bar, text="Auswahl", relief=RAISED).grid(column=1, row=0, padx=5, pady=3, ipadx=10)

def auswahl():
    selection ="Sie wählten Konfig." +str(var.get())
    lable.config(text = selection)

R1 = Radiobutton(tool_bar, text="bearbeiten", variable=var, value=1, command=auswahl).grid(column=1, row=1, padx=5, pady=5)

R2 = Radiobutton(tool_bar, text="bearbeiten", variable=var, value=2, command=auswahl).grid(column=1, row=2, padx=5, pady=5)

R3 = Radiobutton(tool_bar, text="bearbeiten", variable=var, value=3, command=auswahl).grid(column=1, row=3, padx=5, pady=5)

R4 = Radiobutton(tool_bar, text="bearbeiten", variable=var, value=4, command=auswahl).grid(column=1, row=4, padx=5, pady=5)

Label(tool_bar, text="Name").grid(column=0, row=1, padx=5, pady=5)
Label(tool_bar, text="IP").grid(column=0, row=2,padx=5, pady=5)
Label(tool_bar, text="Port").grid(column=0, row=3, padx=5, pady=5)
Label(tool_bar, text="URL").grid(column=0, row=4, padx=5, pady=5)

lable = Label(window)
window.mainloop()

