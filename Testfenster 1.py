import tkinter as tk
from tkinter import *
import tkinter.messagebox



window = tk.Tk()

window.title("Testfenster")
window.geometry("400x200")
frm = tk.Frame(window)
frm.grid()
var = IntVar()


L1 = Label (window, text="Feld 1").grid(column=0, row=0)
E1 = Entry (window, bd =5).grid(column =1, row=0)
L1_1 = Label (window, text="Eingabe von Text NR.1").grid(column=3, row=0)

L2 = Label (window, text ="Feld 2").grid(column = 0, row =1)
E2 = Entry (window, bd = 5).grid(column = 1, row = 1)
L2_1 = Label (window, text="Eingabe von Text NR.2").grid(column=3, row=1)

def auswahl():
    selection ="Sie wählten Konfig." +str(var.get())
    lable.config(text = selection)

R1 = Radiobutton(window, text="Konfig 1", variable=var, value=1, command=auswahl).grid(column=1, row=4)

R2 = Radiobutton(window, text="Konfig 2", variable=var, value=2, command=auswahl).grid(column=1, row=5)

R3 = Radiobutton(window, text="Konfig 3", variable=var, value=3, command=auswahl).grid(column=1, row=6)

 
def bestätigt():
    tk.messagebox.showinfo (title="Bestätigung", message="Ihre Eingabe wurde übermittelt")
B1 = Button(window, text="Bestätigen", command=bestätigt).grid(column=0, row=8)

lable= Label(window)
window.mainloop()
