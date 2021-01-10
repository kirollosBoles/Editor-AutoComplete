# import pandas as pd
import operator


# list.sort(key=operator.itemgetter(1))
class TrieNode:
    def __init__(self, prefix):
        self.prefix = prefix
        self.map = {}
        self.eow = (False, 0)


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

            if (i not in Parent_pointer.map.keys()):
                Parent_pointer.map[i] = TrieNode(key[0:indexs + 1])

            Parent_pointer = Parent_pointer.map[i]
            indexs += 1

        Parent_pointer.eow = (True, 0)

    def get_words_by_prefix(self, prefix):
        Parent_pointer = self.Trie
        resluts = []
        for i in prefix:

            if (i not in Parent_pointer.map.keys()):
                return resluts
            else:
                Parent_pointer = Parent_pointer.map[i]

        self.find_all_sug_dfs(Parent_pointer, resluts)
        return resluts

    def find_all_sug_dfs(self, current_node, result):
        if (current_node.eow[0]):
            result.append((current_node.prefix, current_node.eow[1]))
        for key, value in current_node.map.items():
            if not value == None:
                self.find_all_sug_dfs(value, result)

    def update_wieght(self, word_to_be_updated):
        Parrent_node = self.Trie
        for i in word_to_be_updated:
            if (not Parrent_node.map[i]):
                return False
            Parrent_node = Parrent_node.map[i]
        bool, weight = Parrent_node.eow
        weight += 1
        Parrent_node.eow = (True, weight)


keys = ["yield", "with", "while", "try", "return", "raise", "pass", "or", "not", "nonlocal", "None", "lambda", "is",
        "import", "from", "for", "except"
    , "True", "False", "continue",
        "class", "assert", "else",
        "if", "elif", "finally",
        "for", "from", "global",
        "import", "in", "def", "del", "as"]

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
from tkinter.ttk import Treeview
import sys

dir_path = os.getcwd() + "dir_widget.py"
sys.path.insert(1, dir_path)
import dir_widget as dir
import glob
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
user_defined_list = []
intialized = True
a = list(string.printable)[0:-5]
b = ['Up', 'Left', 'Down', 'Return']
num_area_counter = 1


# events functions
def listen(event):
    cursor_pos = txt.index("insert")
    list_of_positions = cursor_pos.split('.')
    #print(int(txt.index('end').split('.')[0]) - 1)
    global xTBox
    global yTBox
    global intialized
    global user_defined_list
    if event.char in a or event.keysym in b:

        global last_word
        global flag
        global no_list
        global words
        global num_area_counter
        if flag and event.char in a:
            no_list = True
            init_lb()
            flag = False

        if event.keysym == 'Down':
            lb.focus_set()

        if event.char != ' ' and event.keysym != 'Return' and event.keysym != 'Tab':
            last_word += event.char
            leng = len(words)
            list_of_tuple = testing.get_words_by_prefix(last_word)
            list_of_tuple.sort(key=operator.itemgetter(1))
            words = [x[0] for x in list_of_tuple]
        else:
            lb.destroy()
            intialized = FALSE
            if not (last_word in keys):
                if not (last_word in user_defined_list):
                    if ('=' in last_word):
                        # myString.find('s')
                        last_index = last_word.find('=')
                        last_word = last_word[0:last_index]
                    if ('(' in last_word):
                        # myString.find('s')
                        last_index = last_word.find('(')
                        last_word = last_word[0:last_index]
                    testing.Insert_word(last_word)

                    user_defined_list.append(last_word)
                else:
                    testing.update_wieght(last_word)
            else:
                ending_tag = list_of_positions[0] + '.' + str(int(list_of_positions[1]))
                starting_tag = list_of_positions[0] + '.' + str(int(list_of_positions[1]) - len(last_word))
                txt.tag_add("tag", starting_tag, ending_tag)
                txt.tag_config("tag", foreground="blue")
            last_word = ''
            no_list = False
            flag = True

    if event.keysym == 'Return':
        numarea.config(state=NORMAL)
        num_area_counter += 1
        numarea.insert(str(num_area_counter + 1) + '.0', '\n' + str(num_area_counter))
        numarea.config(state=DISABLED)
        last_word = ''
    if event.keysym != 'Down':
        if event.keysym != 'BackSpace':
            xTBox = 8 * (int(list_of_positions[1]) + 1)
        else:
            if (xTBox != 0):
                xTBox = 8 * (int(list_of_positions[1]) + 1)
        yTBox = int(list_of_positions[0]) + 16 * int(list_of_positions[0])
    if event.keysym == 'BackSpace':
        # print(last_word + 'm')
        # if last_word == '\n':
        # print(last_word + 'i')
        # last_word = ''
        last_word = last_word[0:len(last_word) - 1]
        list_of_tuple = testing.get_words_by_prefix(last_word)
        list_of_tuple.sort(key=operator.itemgetter(1))

        # words = testing.get_words_by_prefix(last_word)
        words = [x[0] for x in list_of_tuple]
        #print(xTBox)
        if not (xTBox <= 0):
            xTBox -= 8
            yTBox = int(list_of_positions[0]) + 16 * int(list_of_positions[0])

        else:
            # print(xTBox)

            if num_area_counter > 1:
                numarea.config(state=NORMAL)
                num_area_counter -= 1
                numarea.delete(str(num_area_counter + 1) + '.0', END)
                # print(str(num_area_counter)+'.0')
                numarea.config(state=DISABLED)
            xTBox = list_of_positions[1]
            # print(xTBox)
    if not flag:
        if last_word != '':
            if not intialized:
                init_lb()
                intialized = True
            lb.place(x=xTBox, y=yTBox)
            if event.keysym:
                lb.delete(0, END)
                if words != []:
                    if intialized == FALSE:
                        init_lb()
                        intialized = True
                    for x in words:
                        counter = 0
                        lb.insert(counter, x)
                        counter += 1
                else:
                    lb.destroy()
                    intialized = FALSE
        else:
            lb.destroy()
            intialized = False


def onselect(event):
    # Note here that Tkinter passes an event object to onselect()

    cursor_pos = txt.index("insert")
    spliting = cursor_pos.split('.')
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    s = txt.get("1.0", 'end-1c')
    count_row = s.count("\n") + 1
    sAux = s.replace('\n', ' ')  # make string aux to specify num of words
    list_of_words = sAux.split(' ')

    len_string = len(sAux)
    len_last_word = len(list_of_words[-1])

    deletin_word = str(count_row) + '.' + str(int(spliting[1]) - len_last_word)
    words.insert(0, list_of_words[-1])
    txt.delete(deletin_word, END)
    print(deletin_word)
    if (int(spliting[1]) - len_last_word) == 0 and cursor_pos[0] != '1':
        value = '\n' + value
    txt.insert(END, value)
    cursor_pos = txt.index("insert")
    last_word = value
    list_of_positions = cursor_pos.split('.')
    print(last_word)
    if last_word[0] == '\n':
        last_word= last_word[1:]
    if last_word in keys :
        ending_tag = list_of_positions[0] + '.' + str(int(list_of_positions[1]))
        starting_tag = list_of_positions[0] + '.' + str(int(list_of_positions[1]) - len(last_word))
        txt.tag_add("tag", starting_tag, ending_tag)
        txt.tag_config("tag", foreground="blue")

def selectfirst(event):
    lb.select_set(0)
    a = lb.curselection()


def lb_binds(event):
    global flag
    if event.keysym == 'Return':
        onselect(event)
        txt.focus_set()
        lb.destroy()
        intialized = False
        flag = True

    if event.keysym == 'Down':
        a = lb.curselection()
        print(a)
        lb.select_set(a[0] - 1)
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
    editmenu.add_command(label="Switch mode", command=switchmode)
    menubar.add_cascade(label="Edit", menu=editmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About", command=infobox)
    menubar.add_cascade(label="Help", menu=helpmenu)

    return menubar


def infobox():
    messagebox.showinfo("Info", "This application was created by Small Bug Team\n Version 0.5B")


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
        cmdstr = "py " + '"' +savepath +'"' + " > " + outputpath + " 2>&1"
        os.system(cmdstr)
        stream = open(outputpath)
        text = stream.read()
        runtxt.config(state=NORMAL)
        runtxt.delete(1.0, "END")
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


def viewall(*args):
    global tx, tx2
    txt.yview(*args)
    numarea.yview(*args)


def OnMouseWheel(event):
    txt.yview("scroll", event.delta, "units")
    numarea.yview("scroll", event.delta, "units")


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

txt = Text(mainFrame, width=161, height="29")

txt.bind('<Key>', listen)

numarea = Text(mainFrame, width=3, height=29)
numarea.place(x=200, y=0)
numarea.insert('1.0', '1')
numarea.config(state=DISABLED)

secondFrame = Frame(root, bd=1, width=RWidth, height=str((1 / 2) * frameh))
secondFrame.place(x=0, y=frameh + 2)
runtxt = Text(secondFrame, width=RWidth, height=RHeight)
runtxt.config(state=DISABLED)

scroll = Scrollbar(mainFrame, command=viewall)
scroll.config()
# scroll.place(x=RWidth - 20, y=1)
# scroll.pack(mainFrame,side=RIGHT, fill=Y)

scroll.place(x=1348, y=0)
txt.place(x=230, y=0)
txt.bind("<MouseWheel>", OnMouseWheel)
numarea.bind("<MouseWheel>", OnMouseWheel)
txt['yscrollcommand'] = scroll.set
numarea['yscrollcommand'] = scroll.set

# scroll.config(command=txt.yview)
runtxt.pack()

runtxt.config(state=DISABLED)
txt['yscrollcommand'] = scroll.set
numarea['yscrollcommand'] = scroll.set

defaultcolor = toolbar["bg"]  # storing the original color
txt.focus_set()
menubar = createMenu()
lb = Listbox(txt, name='lb')
lb.bind('<FocusIn>', selectfirst)
lb.bind('<FocusOut>', lambda e: lb.selection_clear(0, END))
lb.bind('<Key>', lb_binds)
lb.bind('<<ListboxSelect>>', onselect)

tree = Treeview(mainFrame, columns=("fullpath", "type", "size"), displaycolumns="", height="29")

tree.heading("#0", text="Directory Structure", anchor='w')
# tree.heading("size", text="File Size", anchor='w')
tree.column("size", stretch=0, width=100)


def selectItem(event):
    global savepath
    curItem = tree.focus()
    if tree.item(curItem)["values"]!="":
        selectionpath = tree.item(curItem)["values"][0]
        if selectionpath[-3:] == ".py":

            savepath = selectionpath
            myfile = open(selectionpath, 'r')
            text = myfile.read()
            txt.delete(1.0, "end-1c")
            txt.insert(1.0, text)
        elif selectionpath[-4:] == ".txt":
            myfile = open(selectionpath, 'r')
            text = myfile.read()
            txt.delete(1.0, "end-1c")
            txt.insert(1.0, text)




dir.populate_roots(tree)
tree.bind('<<TreeviewOpen>>', dir.update_tree)
tree.bind('<Double-Button-1>', dir.change_dir)
tree.bind('<ButtonRelease-1>', selectItem)

tree.place(x=0, y=0)

root.config(menu=menubar)
root.mainloop()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++import