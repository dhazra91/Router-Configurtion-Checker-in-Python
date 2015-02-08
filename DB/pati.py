# -*- coding: utf-8 -*-
import Tkinter as tk
import eg
import database_creator
from PIL import ImageTk, Image

# from http://effbot.org/tkinterbook/entry.html

def display():
    root.destroy()
    import login

def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
    return entry

def enter(event):
    check_password()

def check_password():
    pass


def main1():
    global root
    root= tk.Tk()
    root.geometry('500x500')
    w = tk.Label(root,text="""Buttons can display multiple lines of text (but only in one font). You can use newlines, or use the wraplength option to make the button wrap text by itself. When wrapping text, use the anchor, justify, and possibly padx options to make things look exactly as you wish. An example:
    b = Button(master, text=longtext, anchor=W, justify=LEFT, padx=2)
    To make an ordinary button look like it’s held down, for example if you wish to implement a toolbox of some kind, you can simply change the relief from RAISED to SUNKEN:
    b.config(relief=SUNKEN)""")
    w.pack()
    #frame for window margin
    parent = tk.Frame(root, padx=10, pady=10)
    parent.pack(fill=tk.BOTH, expand=True)

    #button to attempt to login
    b = tk.Button(parent, borderwidth=4, text="OK", justify="left",width=10, pady=8, command=check_password)
    b.pack()

    b = tk.Button(parent, borderwidth=4, text="OK",justify="left", width=10, pady=8, command=check_password)
    b.pack()

    b = tk.Button(parent, borderwidth=4, text="OK",justify="left", width=10, pady=8, command=check_password)
    b.pack()

    #password.bind('<Return>', enter)

    user.focus_set()
    parent.mainloop()


def main():
    global root
    root= tk.Tk()
    root.geometry('2024x2024')
    root.title('WELCOME FOLKS')

    #frame for window margin
    parent = tk.Frame(root, padx=10, pady=10)
    parent.pack(fill=tk.BOTH, expand=True)
    #button to attempt to login
    #path = "/home/netman/Fall2014/himu.jpg"
    path = "/home/netman/Fall2014/comp.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(root, image = img)
    panel.pack(side = "top", fill = "both")

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="10.10.10.10", command=main1)
    filemenu.add_command(label="20.20.20.20", command=main1)

    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    parent.mainloop()

main()


