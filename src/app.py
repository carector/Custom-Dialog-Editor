import textdata

from tkinter import *
from tkinter import ttk

def __init__():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    greeting = ttk.Label(frm, text = "Hello world")
    greeting.pack()
    root.mainloop()
    
__init__()