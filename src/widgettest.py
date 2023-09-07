import textdata
import os
import json
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

# Defs
root = Tk()
td = {}
selectedConvo = -1
selectedDialogLine = -1

# Classes


class ArrayListBox(Frame):
    lbox = Listbox()
    contents = []
    canRename = True

    def __init__(self, master, boxWidth=25, contents=[], canRename=True):
        super().__init__(master)
        self.canRename = canRename
        self.lbox = Listbox(self.master, width=boxWidth,
                            height=15, activestyle=DOTBOX)
        self.lbox.bind("<Button-3>", self.convoBoxRightClick)

        self.contents = contents
        for c in self.contents:
            self.lbox.insert(self.lbox.size(), c)

        self.lbox.pack(side=LEFT, fill=BOTH)

        scroll = Scrollbar(self.master)
        scroll.pack(side=RIGHT, fill=BOTH)
        self.lbox.config(yscrollcommand=scroll.set)
        scroll.config(command=self.lbox.yview)

    def insert(self, index, value):
        self.lbox.insert(index, value)

    def insert(self, value):
        self.lbox.insert(self.lbox.size(), value)

    def clear(self):
        self.lbox.delete(0, 'end')

    def convoBoxRightClick(self, event):
        popup = Menu(self, tearoff=False)
        popup.add_command(label="Insert new", command=showRenameConvoTextbox)
        popup.add_separator()

        # Rename/duplicate/delete only available if an entry exists
        cmdState = 'active'
        if self.lbox.size() == 0:
            cmdState = 'disabled'
        if self.canRename:
            popup.add_command(label="Rename", state=cmdState)
        popup.add_command(label="Duplicate", state=cmdState)
        popup.add_command(label="Delete", state=cmdState)
        popup.tk_popup(x=event.x_root, y=event.y_root)
        # self.lbox.select_clear(0)
        # self.lbox.activate(self.lbox.nearest(event.y_root))

    def rename(self, index):
        print("Nah")


# Widget defs
menubar = Menu(root)

centerframe = Frame(root, padx=10, pady=10)
convoFrame = LabelFrame(centerframe, text="Conversations", bg="gray",
                        fg="white", padx=15, pady=5)
convoArrayListBox = ArrayListBox(convoFrame)

dialogLineFrame = LabelFrame(
    centerframe, text="Dialog lines", bg="lightgray", fg="black", padx=15, pady=5)
dialogLineBox = ArrayListBox(dialogLineFrame, canRename=False, boxWidth=50)

dialogSettingsFrame = Frame(centerframe, padx=15, pady=5)
singleLineSettingsFrame = LabelFrame(
    dialogSettingsFrame, text="Dialog line settings", bg="white", fg="black", padx=15, pady=5)
textboxFrame = LabelFrame(singleLineSettingsFrame, text="Text",
                          bg="white", fg="black", padx=15, pady=5)
textbox = Text(textboxFrame, bg="white", height=4,
               width=32, padx=2, pady=2, wrap="none")



# Commands


def onNew():
    global td
    td = textdata.TextData()
    updateDialogLineBoxContents()


def onOpen():
    global td
    currdir = "D:\_ACTIVE UNITY PROJECTS\RogueMoon\Assets\Resources"  # Temporary
    root.filename = filedialog.askopenfilename(
        initialdir=currdir, title="Select file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))

    s = open(root.filename, 'r').read()
    data = json.loads(s)

    # Need to restructure data if its in the old json format
    # if 'dialog' in data['conversations'][0]:
    #     td.filename = data['filename']
    #     td.conversations = data['conversations']
    #     for x in range(len(td.conversations)):
    #         lines = []
    #         for d in data['conversations'][x]['dialog']:
    #             for s in d['sentences']:
    #                 lines.append(s)
    #         convo = textdata.Conversation
    #         convo.dialogLines = lines
    #         td.conversations[x] = convo
    # else:
    td = data

    # Convos setup
    convoArrayListBox.clear()
    for c in td['conversations']:
        convoArrayListBox.insert(c['conversationId'])

    # Dialog line setup
    updateDialogLineBoxContents(0)


def onSave():
    global td
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

def onAddConvo(event):
    w = event.widget


def onSwitchConvo(event):
    global selectedConvo
    w = event.widget
    index = -1
    if w.curselection():
        index = int(w.curselection()[0])
    if index == -1:
        return
    selectedConvo = index
    updateDialogLineBoxContents(index)


def onAddDialogLine(event):
    w = event.widget


def updateDialogLineBoxContents(index):
    # Update dialog line box contents
    dialogLineBox.clear()
    rootConvo = td['conversations'][index]
    for d in rootConvo['dialog']:
        for s in d['sentences']:
            dialogLineBox.insert(s['text'])


def onSwitchDialogLine(event):
    global selectedDialogLine
    w = event.widget
    index = -1
    if w.curselection():
        index = int(w.curselection()[0])
    if index == -1:
        return
    selectedDialogLine = index
    updateDialogLineSettingsContents(index)


def updateDialogLineSettingsContents(index):
    selectedDialogLine = index
    s = td['conversations'][selectedConvo]['sentences'][selectedDialogLine]
    textbox.delete(1.0, "END")
    textbox.insert("END", s['text'])

def showRenameConvoTextbox():
    global popupRoot
    popupRoot = Tk()

    convoNameFrame = LabelFrame(
        popupRoot, text="Enter conversation ID", bg="grey", fg="white", padx=15, pady=5)
    convoNameTextbox = Text(convoNameFrame, bg="white", height=1,
               width=24, padx=2, pady=2, wrap="none")

    def onConfirmName():
        print("Yeah")
        s = convoNameTextbox.get("1.0", END)
        convoArrayListBox.insert(s)
        convos = td['conversations']
        convos.append({'conversationId': s, 'dialogLines': []})
        popupRoot.destroy()

    w = 320
    h = 96
    rootX = (root.winfo_screenwidth()/2) - (1050/2) + root.winfo_x()
    rootY = (root.winfo_screenheight()/2) - (300/2) + root.winfo_y()
    popupRoot.geometry('%dx%d+%d+%d' % (w, h, rootX, rootY))
    popupRoot.resizable(False, False)
    popupRoot.title("Enter conversation ID")
    convoNameFrame.grid(column=0, row=0)
    convoNameTextbox.grid(column=0, row=0, padx=5)
    convoNameButton = Button(convoNameFrame, text="OK", padx=15, command=onConfirmName)
    convoNameButton.grid(column=1, row=0)


def onExit():
    popupRoot.destroy()
    root.destroy()
    quit()


# Layout
root.geometry("1050x300")
root.title("Mountain dialog editor")
#root.resizable(False, False)

# Toolbar
root.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=False)
fileMenu.add_command(label="New", command=onNew)
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

centerframe.pack(anchor=W)

# Conversations box
convoFrame.grid(row=0, column=0)
convoArrayListBox.lbox.bind("<<ListboxSelect>>", onSwitchConvo)
convoArrayListBox.lbox.bind("<<ListboxInsert")

# Dialog line selector
dialogLineFrame.grid(row=0, column=1)
dialogLineBox.lbox.bind("<<ListboxSelect>>", onSwitchDialogLine)

# Settings frames
dialogSettingsFrame.grid(row=0, column=2)
singleLineSettingsFrame.grid(row=0, column=0, sticky=N)
#convoSettingsFrame.grid(row=1, column=0, sticky=S)

# Dialog line settings
textboxFrame.grid(row=0, column=0)
textbox.grid(row=0, column=0, sticky=W)

portraitFrame = LabelFrame(
    singleLineSettingsFrame, text="Portrait", bg="white", fg="black", padx=15, pady=6)
portraitFrame.grid(row=0, column=1)
portrait = ImageTk.PhotoImage(Image.open(
    "D:/_Code projects/MountainDialogEditor/src/res/Bo.png").resize((64, 64)))
portraitButton = Button(portraitFrame, image=portrait,
                      relief=GROOVE).grid(row=0, column=1)
fontFrame = LabelFrame(
    singleLineSettingsFrame, text="Font", bg="white", fg="black", padx=15, pady=6)
fontFrame.grid(row=1, column=0)
fontButton = Button(fontFrame, text="Coming soon?").grid(row=0, column=0)

portraitPositionFrame = LabelFrame(
    singleLineSettingsFrame, text="Portrait position", bg="white", fg="black", padx=15, pady=6)
portraitPositionFrame.grid(row=1, column=1)
leftPortraitButton = Button(portraitPositionFrame, text="   L   ", bg="black")
rightPortraitButton = Button(portraitPositionFrame, text="   R   ", bg="white")
leftPortraitButton.grid(row=0, column=0)
rightPortraitButton.grid(row=0, column=1)

# Conversation settings
#convoNameFrame.grid(column=0, row=0)
#convoNameTextbox.grid(column=0, row=0, sticky=W)

#fontLabel = Label(fontFrame).grid(row=0, column=1)

# Cheat sheet
# cheatSheetFrame = LabelFrame(dialogSettingsFrame, text="Cheat sheet", bg="white", fg="black", padx=15, pady=5)
# cheatlabel = Label(cheatSheetFrame, text="Was wa a wa").grid(row=0, column=0)
# cheatSheetFrame.grid(row=1, column=0, sticky=S)

root.mainloop()
