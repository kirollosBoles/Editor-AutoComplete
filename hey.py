"""A directory browser using Ttk Treeview.

Based on the demo found in Tk 8.5 library/demos/browse
"""
import os
import glob
import tkinter
from tkinter import *
from tkinter.ttk import *

def populate_tree(tree, node):
    if tree.set(node, "type") != 'directory':
        return

    path = tree.set(node, "fullpath")
    tree.delete(*tree.get_children(node))

    parent = tree.parent(node)
    special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

    for p in special_dirs + os.listdir(path):
        ptype = None
        p = os.path.join(path, p).replace('\\', '/')
        if os.path.isdir(p): ptype = "directory"
        elif os.path.isfile(p): ptype = "file"

        fname = os.path.split(p)[1]
        id = tree.insert(node, "end", text=fname, values=[p, ptype])

        if ptype == 'directory':
            if fname not in ('.', '..'):
                tree.insert(id, 0, text="dummy")
                tree.item(id, text=fname)

def populate_roots(tree):
    dir = os.path.abspath('.').replace('\\', '/')
    node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
    populate_tree(tree, node)

def update_tree(event):
    tree = event.widget
    populate_tree(tree, tree.focus())

def change_dir(event):
    tree = event.widget
    node = tree.focus()
    if tree.parent(node):
        path = os.path.abspath(tree.set(node, "fullpath"))
        if os.path.isdir(path):
            os.chdir(path)
            tree.delete(tree.get_children(''))
            populate_roots(tree)

def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)

root = tkinter.Tk()

vsb = Scrollbar(orient="vertical")
hsb = Scrollbar(orient="horizontal")

tree = Treeview(columns=("fullpath", "type", "size"),displaycolumns="")


tree.heading("#0", text="Directory Structure", anchor='w')
# tree.heading("size", text="File Size", anchor='w')
tree.column("size", stretch=0, width=100)

def selectItem(event):
    curItem = tree.focus()
    print (tree.item(curItem))

populate_roots(tree)
tree.bind('<<TreeviewOpen>>', update_tree)
tree.bind('<Double-Button-1>', change_dir)
tree.bind('<ButtonRelease-1>', selectItem)
tree.bind('<Enter>', selectItem)


tree.grid(column=0, row=0, sticky='nswe')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
