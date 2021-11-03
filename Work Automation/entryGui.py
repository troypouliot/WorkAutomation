from tkinter import *

root = Tk()




def myclick():
    hello = 'Hello ' + e.get()
    myLabel = Label(root, text=hello)
    myLabel.pack()

e = Entry(root, width=50)
e.pack()



myButton = Button(root, text='Enter your name', command=myclick, pady=50)
myButton.pack()



root.mainloop()



