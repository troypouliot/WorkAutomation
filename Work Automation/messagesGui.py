from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()
root.title('Message Box')
root.iconbitmap('car.ico')

#   showinfo, showwarning, showerror, askquestion, askokcancel, askyesno

def popupInfo():
    response = messagebox.showinfo("INFO", "This is a info box")
    print(response)
def popupWarning():
    response = messagebox.showwarning("WARNING", "This is a warning box")
    print(response)
def popupError():
    response = messagebox.showerror("ERROR", "This is a error box")
    print(response)
def popupaskquestion():
    response = messagebox.askquestion("ASK QUESTION", "This is a ask question box")
    print(response)
def popupaskokcancel():
    response = messagebox.askokcancel("ASK OK CANCEL", "This is a ask ok cancel box")
    print(response)
def popupaskyesno():
    response = messagebox.askyesno("ASK YES NO", "This is a ask yes no box")
    print(response)

def popupaskretrycancel():
    response = messagebox.askretrycancel("ASK RETRY CANCEL", "This is a ask retry cancel box")
    print(response)

def popupaskyesnocancel():
    response = messagebox.askyesnocancel("ASK YES NO CANCEL", "This is a ask yes no cancel box")
    print(response)

Button(root, text="Info Message", command=popupInfo).pack()
Button(root, text="Warning Message", command=popupWarning).pack()
Button(root, text="Error Message", command=popupError).pack()
Button(root, text="Ask Question Message", command=popupaskquestion).pack()
Button(root, text="Ask ok cancel", command=popupaskokcancel).pack()
Button(root, text="Ask yes no", command=popupaskyesno).pack()
Button(root, text="Ask retry cancel", command=popupaskretrycancel).pack()
Button(root, text="Ask yes no cancel", command=popupaskyesnocancel).pack()



root.mainloop()



