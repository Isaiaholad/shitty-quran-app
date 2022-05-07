import tkinter as tk
from tkinter import messagebox 
from tkinter.constants import ACTIVE
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
from pygame import mixer
from QuoranDb import *


class Quoran(tk.Frame):
    def __init__(self, master):
        super(Quoran, self).__init__(master)
        mixer.init()
        mixer.music.load("bgtune.mp3")
        mixer.music.play(loops=100000,start=1.1)
        self.bg = tk.PhotoImage(file = "bg.png")
        self.nextimg = tk.PhotoImage(file = "next.png")
        self.previmg = tk.PhotoImage(file="prev.png")
        self.bglbl = tk.Label(self.master, image=self.bg).place(x=0, y=0)

        style = tk.ttk.Style()
        style.theme_settings("default", {
            "TCombobox": {
                "configure": {"padding": 5},
                "map": {
                    "background": [("active", "green2"), ("!disabled", "green4")],
                    "fieldbackground": [("!disabled", "green3")],
                    "foreground": [("focus", "OliveDrab1"), ("!disabled", "OliveDrab2")]
                }
            }
        })

        tk.Label(self.master, text="Chapter ", font=("Elephant", 15)).place(x=190, y=20)
        tk.Label(self.master, text=" Verse  ", font=("Elephant", 15)).place(x=190, y=70)
        tk.Button(self.master, text="<<", image=self.previmg, font=("Segoe Script", 20), command=self.prev).place(x=40, y=50)
        tk.Button(self.master, text=">>", image=self.nextimg, font=("Segoe Script", 20), command=self.next).place(x=480, y=50)
        self.contexteng = ScrolledText(self.master, height=5, width=35, font=("consolas", 15, "bold"), bg="white", fg="green",
                                       relief=tk.SUNKEN, state=tk.DISABLED, wrap=tk.WORD)
        self.contexteng.place(x=100, y=170)
        self.contextarb = ScrolledText(self.master, height=5, width=35, insertbackground="#fff", font=("consolas", 15, "bold"), fg="green",
                                       relief=tk.SUNKEN, state=tk.DISABLED, wrap=tk.WORD)
        self.contextarb.place(x=100, y=370)
        self.chapterbox = Combobox(self.master, width=10, font=("Elephant", 15), background="white", foreground="grey")
        self.chapterbox.place(x=300, y=20)
        self.chapterbox.bind(sequence="<<ComboboxSelected>>", func=self.chapterchanged)
        self.chapterbox.bind(sequence="<KeyRelease>", func=self.chapterchanged)
        self.chapterbox.configure(values=[x for x in range(1, 115)])
        self.versebox = Combobox(self.master, width=10, font=("Elephant", 15), background="white", foreground="grey" )
        self.versebox.place(x=300, y=70)
        self.versebox.bind(sequence="<<ComboboxSelected>>", func=self.versechanged)
        self.versebox.bind(sequence="<KeyRelease>", func=self.versechanged)
        self.addbookmarkbtn = tk.Button(text="ADD BOOKMARK", command=self.addbookmark)
        self.addbookmarkbtn.place(x=150, y=525)
        tk.Button(text="VIEW BOOKMARKS", command=self.viewbookmark).place(x=310, y=525)
        self.currentchapter = "1"
        self.currentverse = "1"
        self.versecount = "1"
        self.chapcount = "1"
        self.versecontent_eng = ""
        self.versecontent_arb = ""
        self.bookmarkWindow = ""
        self.bookmarklist = ""

    def chapterchanged(self, _=""):
        self.currentchapter = self.chapterbox.get()
        self.versecount = getAllVerse(self.currentchapter)
        self.versebox.set(1)
        self.versebox["values"] = [x for x in range(1, self.versecount+1)]
        self.currentverse = self.versebox.get()
        self.getcontent()

    def versechanged(self, _=""):
        self.currentverse = self.versebox.get()
        self.getcontent()

    def getcontent(self):
        self.currentchapter = self.chapterbox.get()
        self.currentverse = self.versebox.get()
        if checkBookmark(self.currentchapter, self.currentverse):
            self.addbookmarkbtn.configure(text="BOOKMARKED")
        else:
            self.addbookmarkbtn.configure(text="ADD BOOKMARK")
        self.versecontent_eng = getEngContext(self.currentchapter, self.currentverse)
        self.contexteng.configure(state=tk.NORMAL)
        self.contexteng.delete("1.0", tk.END)
        self.contexteng.insert(tk.END, self.versecontent_eng)
        self.contexteng.configure(state=tk.DISABLED)

        self.versecontent_arb = getArbContext(self.currentchapter, self.currentverse)
        self.contextarb.configure(state=tk.NORMAL)
        self.contextarb.delete("1.0", tk.END)
        self.contextarb.insert(tk.END, self.versecontent_arb)
        self.contextarb.configure(state=tk.DISABLED)

    def prev(self):
        try:
            if int(self.versebox.get()) == 1:
                self.chapterbox.current(int(self.chapterbox.get()) - 2)
                self.chapterchanged()
            else:
                self.versebox.current(int(self.versebox.get())-2)
                self.versechanged()
        except IndexError:
            pass   # Reached the last index

    def next(self):
        try:
            if int(self.versebox.get()) == getAllVerse(self.chapterbox.get()):
                self.chapterbox.current(int(self.chapterbox.get()))
                self.chapterchanged()
            else:
                self.versebox.current(int(self.versebox.get()))
                self.versechanged()
        except IndexError:
            pass   # Reached the last index

    def addbookmark(self):
        self.currentchapter = self.chapterbox.get()
        self.currentverse = self.versebox.get()
        if checkBookmark(self.currentchapter, self.currentverse):
            removeBookmark(self.currentchapter, self.currentverse)
            messagebox.showinfo("Success",
                                f"chapter {self.currentchapter} verse {self.currentverse} has been removed Bookmarks")
            self.getcontent()
        else:
            addToBookmark(self.currentchapter, self.currentverse)
            messagebox.showinfo("Success",
                                f"chapter {self.currentchapter} verse {self.currentverse} has been added to Bookmark")
            self.getcontent()

    def viewbookmark(self):
        self.bookmarkWindow = tk.Toplevel(self.master)
        self.bookmarkWindow.geometry("400x400+100+100")
        self.bookmarkWindow.title("Bookmarks")
        self.bookmarklist = tk.Listbox(self.bookmarkWindow, width=50, height=20)
        self.bookmarklist.bind("<Double-Button-1>", func=self.viewbookmarked)
        self.bookmarklist.place(x=40, y=20)
        tk.Button(self.bookmarkWindow, text="VIEW", command=self.viewbookmarked).place(x=100, y=350)
        tk.Button(self.bookmarkWindow, text="REMOVE", command=self.removebookmarked).place(x=250, y=350)
        allbookmarked = getAllBookmarked()
        for i, b in enumerate(allbookmarked):
            chp, vrs = b
            self.bookmarklist.insert(i, f"chapter {chp} verse {vrs}")

    def viewbookmarked(self):
        self.chapterbox.set((self.bookmarklist.get(ACTIVE)).split(" ")[1])
        self.versebox.set((self.bookmarklist.get(ACTIVE)).split(" ")[3])
        self.bookmarkWindow.destroy()
        self.getcontent()

    def removebookmarked(self):
        chp = (self.bookmarklist.get(ACTIVE)).split(" ")[1]
        vrs = (self.bookmarklist.get(ACTIVE)).split(" ")[3]
        removeBookmark(chp, vrs)
        self.bookmarkWindow.destroy()
        self.viewbookmark()


window = tk.Tk()
frame = Quoran(window)
window.resizable(False, False)
window.geometry("600x600+5+5")
window.title("Q U O R A N")
window.mainloop()
