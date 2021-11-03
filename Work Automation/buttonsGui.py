import tkinter
from tkinter import *

root = Tk()


def myclick():
    myLabel = Label(root, text='You clicked me')
    myLabel.pack()


root.geometry("300x300")

optionsList = ('Nightlight', 'Window Cling', 'Option 3', 'Option 4')
myButton = Button(root, text='Click Me', command=myclick, pady=50)
var = tkinter.StringVar()
var.set(optionsList[0])
my_option = OptionMenu(root, var, *optionsList)
myButton.pack()
my_option.pack()
Label(root, textvariable=var).pack()
root.mainloop()
