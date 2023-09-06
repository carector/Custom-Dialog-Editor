import textdata
import os
import json
from tkinter import *
from tkinter import filedialog

# Defs
td = textdata.TextData()


def onNew():
    td = textdata.TextData()


def onOpen():
    currdir = "D:\_ACTIVE UNITY PROJECTS\RogueMoon\Assets\Resources"  # Temporary
    root.filename = filedialog.askopenfilename(
        initialdir=currdir, title="Select file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))

    s = open(root.filename, 'r').read()
    td = json.loads(s)


def onSave():
    if root.filename != '':
        onSaveAs
    else:
        s = open(root.filename, 'w')
        if td != "":
            json.dump(td, s)
        s.close()


def onSaveAs():
    currdir = "D:\_ACTIVE UNITY PROJECTS\RogueMoon\Assets\Resources"  # Temporary
    path = filedialog.asksaveasfilename(
        initialdir=currdir, title="Select file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")), defaultextension="*.json")

    s = open(path, 'w')
    root.filename = path
    if td != "":
        json.dump(td, s)
    s.close()
    return


def onExit():
    quit()


# Widgets
root = Tk()

root.geometry("1366x565")
# root.resizable(False, False)

# Toolbar
menubar = Menu(root)
root.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=False)
fileMenu.add_command(label="New")
fileMenu.add_command(
    label="Open",
    command=onOpen
)
fileMenu.add_separator()
fileMenu.add_command(
    label="Save",
    command=onSave
)
fileMenu.add_command(
    label="Save as",
    command=onSaveAs
)
fileMenu.add_separator()
fileMenu.add_command(
    label="Exit",
    command=onExit
)

menubar.add_cascade(label="File", menu=fileMenu)

centerframe = Frame(root, padx=10, pady=10)
centerframe.pack(anchor=W)


class ArrayListBox(Frame):
    lbox = Listbox()
    contents = []

    def __init__(self, master, contents = []):
        super().__init__(master)
        self.lbox = Listbox(self.master, width=25,
                            height=30, activestyle=DOTBOX)
        self.lbox.bind("<Button-3>", self.convoBoxRightClick)
        
        self.contents = contents
        for c in self.contents:
            self.lbox.insert(self.lbox.size(), c)
        
        self.lbox.pack(side=LEFT, fill=BOTH)

        scroll = Scrollbar(self.master)
        scroll.pack(side=RIGHT, fill=BOTH)
        self.lbox.config(yscrollcommand=scroll.set)
        scroll.config(command=self.lbox.yview)

    def convoBoxRightClick(self, event):
        popup = Menu(root, tearoff=False)
        popup.add_command(label="Insert new")
        popup.add_separator()
        popup.add_command(label="Rename")
        popup.add_command(label="Duplicate")
        popup.add_command(label="Delete")
        popup.tk_popup(x=event.x_root, y=event.y_root)
        #self.lbox.select_clear(0)
        #self.lbox.activate(self.lbox.nearest(event.y_root))

    def rename(self, index):
        print("Nah")


convoFrame = LabelFrame(centerframe, text="Conversations", bg="gray",
                        fg="white", padx=15, pady=5)
convoFrame.grid(row=0, column=0)
convoBox = ArrayListBox(convoFrame, ("Nachos", "Shit", "Fuck", "Asshole"))

# Dialog tab
dialogFrame = LabelFrame(centerframe, text="Dialogs",
                         bg="lightgray", padx=15, pady=5)
dialogFrame.grid(row=0, column=1)
dialogBox = ArrayListBox(dialogFrame, ("Nachos", "Shit", "Fuck", "Asshole"))

sentenceFrame = LabelFrame(centerframe, text="Sentences",
                           bg="white", padx=250, pady=120)

sentenceFrame.grid(row=0, column=2)
t = Text(sentenceFrame, bg="white", height=4,
         width=32, padx=2, pady=2, wrap="none")
t.grid(row=0, column=0, sticky=NW)


root.mainloop()
