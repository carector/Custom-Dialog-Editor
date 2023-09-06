import textdata
import os
import json
import tkinter as tk

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

root = Tk()
root.filename = ""
td = textdata.TextData

class Toolbar(Frame):

    def __init__(self):
        super().__init__()

        # Setup toolbar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # File
        fileMenu = Menu(menubar, tearoff=False)
        fileMenu.add_command(label="New")
        fileMenu.add_command(
            label="Open",
            command=self.onOpen
        )
        fileMenu.add_separator()
        fileMenu.add_command(
            label="Save",
            command=self.onSave
        )
        fileMenu.add_command(
            label="Save as",
            command=self.onSaveAs
        )
        fileMenu.add_separator()
        fileMenu.add_command(
            label="Exit",
            command=self.onExit
        )

        menubar.add_cascade(label="File", menu=fileMenu)

    def onNew(self):
        td = textdata.TextData()

    def onOpen(self):
        currdir = "D:\_ACTIVE UNITY PROJECTS\RogueMoon\Assets\Resources"  # Temporary
        root.filename = filedialog.askopenfilename(
            initialdir=currdir, title="Select file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))

        s = open(root.filename, 'r').read()
        self.td = json.loads(s)
        self.onLoadData()

    def onSave(self):
        if root.filename != '':
            self.onSaveAs
        else:
            s = open(root.filename, 'w')
            if self.td != "":
                json.dump(self.td, s)
            s.close()

    def onSaveAs(self):
        currdir = "D:\_ACTIVE UNITY PROJECTS\RogueMoon\Assets\Resources"  # Temporary
        path = filedialog.asksaveasfilename(
            initialdir=currdir, title="Select file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")), defaultextension="*.json")
        
        s = open(path, 'w')
        root.filename = path
        if self.td != "":
            json.dump(self.td, s)
        s.close()
        return

    def onExit(self):
        self.quit()


class ConversationsBox(Frame):
    langs = ('Java', 'C#', 'C', 'C++', 'Python',
             'Go', 'JavaScript', 'PHP', 'Swift')

    var = tk.Variable(value=langs)

    listbox = tk.Listbox(
        root,
        listvariable=var,
        height=6,
        width=1,
        selectmode=tk.EXTENDED
    )

    listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    scrollbar = ttk.Scrollbar(
        root,
        orient=tk.VERTICAL,
        command=listbox.yview
    )

    listbox['yscrollcommand'] = scrollbar.set

    scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)

    def items_selected(event, self):
        # get selected indices
        selected_indices = self.listbox.curselection()
        # get selected items
        selected_langs = ",".join([self.listbox.get(i)
                                  for i in selected_indices])
        msg = f'You selected: {selected_langs}'
        print(msg)

    listbox.bind('<<ListboxSelect>>', items_selected)



root.geometry("1366x768")
root.title("Mountain dialog editor")

convoFrame = tk.Frame()
convoFrame.pack(side=RIGHT)
toolbar = Toolbar()
convos = ConversationsBox(convoFrame)
root.mainloop()