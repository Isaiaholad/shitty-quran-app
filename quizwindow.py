import tkinter as tk

class Quizwindow(tk.Toplevel):
    def __init__(self, master):
        super(Quizwindow, self).__init__(master)
        tk.LabelFrame(width=400,height=400).place(x=100,y=100)
        questiontxt = tk.Text(self.master, height = 5, width = 30, font=("Elephant",15), relief = tk.RAISED, state = tk.DISABLED, wrap = tk.WORD, selectborderwidth=5)
        questiontxt.place(x=130,y=130)

        

windo = tk.Tk()
windo.geometry("600x600+5+5")
winn = Quizwindow(windo)
windo.mainloop()
        