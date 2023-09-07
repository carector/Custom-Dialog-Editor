from tkinter import *

class DragDropListbox(Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = SINGLE
        Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i

root = Tk()
centerframe = Frame(root)
centerframe.pack(anchor=W)

lb = Listbox(centerframe)
lb.pack(anchor=W)
lb2 = DragDropListbox(lb)
lb2.insert(0, 'hi')
lb2.insert(0, 'gi')
lb2.insert(0, 'bi')
lb2.insert(0, 'ei')

lb2.pack(anchor=W)

root.mainloop()