# import pandas as pd

class TrieNode:
    def __init__(self, prefix):
        self.prefix = prefix
        self.array = [None] * 26
        self.eof = False


class AutoComplete:
    Trie = TrieNode("")

    def __init__(self, words):
        self.Trie = TrieNode("")
        for w in words:
            self.Insert_word(w)

    def Insert_word(self, key):
        Parent_pointer = self.Trie
        indexs = 0
        for i in key:
            index = ord(i) - 97
            if (not Parent_pointer.array[index]):
                Parent_pointer.array[index] = TrieNode(key[0:indexs + 1])

            Parent_pointer = Parent_pointer.array[index]
            indexs += 1

        Parent_pointer.eof = True

    def get_words_by_prefix(self, prefix):
        Parent_pointer = self.Trie
        resluts = []
        for i in prefix:
            index = ord(i) - 97
            if (Parent_pointer.array[index]):
                Parent_pointer = Parent_pointer.array[index]
            else:
                return resluts

        self.find_all_sug_dfs(Parent_pointer, resluts)
        return resluts

    def find_all_sug_dfs(self, current_node, result):
        if (current_node.eof):
            result.append(current_node.prefix)
        for i in current_node.array:
            if not i == None:
                self.find_all_sug_dfs(i, result)


keys = ["yield", "with", "while", "try", "return", "raise", "pass", "or", "not", "nonlocal", "none", "lambda", "is",
        "import", "from", "for", "except"
    , "true", "false", "continue",
        "class", "assert", "else",
        "if", "elif", "finally",
        "for", "from", "global",
        "import", "in", "def", "del"]

testing = AutoComplete(keys)
# ++++++++++++++++++++++++++++++++++++++++++++++++++
# from Tkinter import *
import tkinter
from tkinter import *
from pynput import keyboard
import string
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox

import sys

xTBox = 1
yTBox = 16
flag = True
no_list = False
init_pos = False
defaultcolor = None
savepath = ""
last_word = ''
words = []

a = list(string.printable)[0:-5]
b = ['Up', 'Left', 'Down', 'Return']


# events functions
def listen(event):
    cursor_pos = txt.index("insert")
    list_of_positions = cursor_pos.split('.')
    global xTBox
    global yTBox

    if event.char in a or event.keysym in b:

        global last_word
        global flag
        global no_list
        global words
        if flag and event.char in a:
            no_list = True
            init_lb()
            flag =False

        if event.keysym == 'Down':
            lb.focus_set()

        if event.char != ' ' and event.keysym != 'Return' and event.keysym != 'Tab':
            last_word += event.char
            leng = len(words)
            words = testing.get_words_by_prefix(last_word)
        else:
            last_word = ''
            no_list = False
            lb.destroy()
            flag = True

    if event.keysym != 'Down' and event.keysym != 'BackSpace':
        xTBox = int(list_of_positions[1]) + 8 * int(list_of_positions[1])
        yTBox = int(list_of_positions[0]) + 16 * int(list_of_positions[0])
    if event.keysym == 'BackSpace':
        last_word = last_word[0:len(last_word) - 1]
        words = testing.get_words_by_prefix(last_word)
        if not xTBox < 1 :
            xTBox -= 8
            yTBox = int(list_of_positions[0]) + 16 * int(list_of_positions[0])
    if not flag:
        lb.place(x=xTBox, y=yTBox)
        if event.keysym:
            lb.delete(0, END)
            for x in words:
                counter = 0
                lb.insert(counter, x)
                counter += 1


def onselect(event):
    # Note here that Tkinter passes an event object to onselect()
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    s = txt.get("1.0", 'end-1c')
    # sAux = s.replace('\n', ' ')  # make string aux to specify num of words
    list_of_words = s.split(' ')
    count_row = s.count("\n") + 1
    len_string = len(s)
    len_last_word = len(list_of_words[-1])
    deletin_word = str(count_row) + '.' + str(len_string - len_last_word)
    words.insert(0, list_of_words[-1])
    txt.delete(deletin_word, END)
    txt.insert(END, value)


def selectfirst(event):
    lb.select_set(0)
    a = lb.curselection()
    print(a)

def lb_binds(event):
    global flag
    if event.keysym == 'Return':
        txt.focus_set()
        lb.destroy()
        flag = True
    if event.keysym == 'Down':
        a=lb.curselection()
        print(a)
        lb.select_set(a[0]-1)
        a = lb.curselection()
        print(a[0])



def createMenu():
    def donothing():
        x = 0

    menubar = Menu(root)  # menu things
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=openfile)
    filemenu.add_command(label="Save as", command=saveas)
    filemenu.add_command(label="Save", command=save1)
    filemenu.add_command(label="Clear", command=lambda: txt.delete(1.0, END))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="File", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Dark mode", command=switchmode)
    menubar.add_cascade(label="Edit", menu=editmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About", command=infobox)
    menubar.add_cascade(label="Help", menu=helpmenu)

    return menubar


def infobox():
    messagebox.showinfo("Info", "This application was created by Small Bug Team\n Version 0.2b")


def init_lb():
    lb = Listbox(txt, name='lb')
    lb.bind('<FocusIn>', selectfirst)
    lb.bind('<FocusOut>', lambda e: lb.selection_clear(0, END))

    lb.bind('<Key>', lb_binds)
    lb.bind('<<ListboxSelect>>', onselect)


def run():
    save1()
    if savepath:
        outputpath = "C:\\Users\\ahmed\\Desktop\\output.txt"
        cmdstr = "py " + savepath + " > " + outputpath + " 2>&1"
        os.system(cmdstr)
        stream = open(outputpath)
        text = stream.read()
        runtxt.delete(1.0, "end-1c")
        runtxt.config(state=NORMAL)
        runtxt.insert(1.0, text)
    else:
        saveas()
    runtxt.config(state=DISABLED)


def openfile():
    global savepath
    file = filedialog.askopenfile(mode="r")
    if file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    savepath = str(file.name)
    text = file.read()
    txt.delete(1.0, "end-1c")
    txt.insert(1.0, text)


def saveas():
    global savepath
    f = filedialog.asksaveasfile(mode='w', defaultextension=".py")

    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    savepath = str(f.name)
    text2save = str(txt.get("1.0", 'end-1c'))
    f.write(text2save)
    f.close()

def save1():
    global savepath
    if savepath != "":
        file = open(savepath, 'w+')
        save = txt.get(1.0, "end-1c")
        file.write(save)
        file.close()
    else:
        return saveas()


def switchmode():
    if txt["bg"] == "#2B2B2B":
        txt["bg"] = "#FFF"
        txt["fg"] = "#000"
        toolbar["bg"] = defaultcolor
        txt.config(insertbackground="#000")

    else:

        txt["bg"] = "#2B2B2B"
        toolbar["bg"] = "#808080"
        txt["fg"] = "#D8D8D8"
        txt.config(insertbackground="#FFF")


# //////////////////////////////////////////////////////////////////////////////////////
root = Tk()
root.state('normal')  # maximized window
RWidth = root.winfo_screenwidth()  # take the width of the device
RHeight = root.winfo_screenheight()  # take the height of the device
root.geometry(("%dx%d") % (RWidth, RHeight))  # bye3mel el ab3ad bta3th 3la 7asab el system
toolbar = Frame(root, bd=1, relief=GROOVE)

root.title("Small Bug Team")

img2 = Image.open("resources/open.png")
eimg2 = ImageTk.PhotoImage(img2)
runButton = Button(toolbar, image=eimg2, relief=FLAT, command=openfile)
runButton.image = eimg2
runButton.pack(side=LEFT, padx=2, pady=2)

img1 = Image.open("resources/save.png")
eimg1 = ImageTk.PhotoImage(img1)
saveButton = Button(toolbar, image=eimg1, relief=FLAT, command=save1)
saveButton.image = eimg1
saveButton.pack(side=LEFT, padx=2, pady=2)

img = Image.open("resources/run.png")
eimg = ImageTk.PhotoImage(img)
runButton = Button(toolbar, image=eimg, relief=FLAT, command=run)
runButton.image = eimg
runButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

frameh = int((2 / 3) * int(RHeight))

mainFrame = Frame(root, bd=1, width=RWidth, height=frameh)
mainFrame.pack()

txt = Text(mainFrame, width=169, height="30")

txt.bind('<Key>', listen)

secondFrame = Frame(root, bd=1, width=RWidth, height=str((1 / 2) * frameh))
secondFrame.place(x=0, y=frameh + 2)
runtxt = Text(secondFrame, width=RWidth, height=RHeight)
runtxt.config(state=DISABLED)

scroll = Scrollbar(mainFrame)
scroll.config()
# scroll.place(x=RWidth - 20, y=1)
# scroll.pack(mainFrame,side=RIGHT, fill=Y)
scroll.pack(side="right", fill="y", expand=False)
txt.pack(side="left", fill="both", expand=True)

txt['yscrollcommand'] = scroll.set

scroll.config(command=txt.yview)
runtxt.pack()

runtxt.config(state=DISABLED)
txt['yscrollcommand'] = scroll.set

defaultcolor = toolbar["bg"]  # storing the original color
txt.focus_set()
menubar = createMenu()
lb = Listbox(txt, name='lb')
lb.bind('<FocusIn>', selectfirst)
lb.bind('<FocusOut>', lambda e: lb.selection_clear(0, END))
lb.bind('<Key>', lb_binds)
lb.bind('<<ListboxSelect>>', onselect)

root.config(menu=menubar)
root.mainloop()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
