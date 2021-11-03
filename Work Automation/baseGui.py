from tkinter import *

root = Tk()
root.title("Main Window")

# Create label widget
myLabel = Label(root, text='                    Hello World                         ')
def openwind():
    top = Toplevel()
    top.title("This is the other window")
    Label(top, text="this is the other window").pack()
    Button(top, text="close 2nd window", command=top.destroy).pack()
# Shoving it onto the screen
myLabel.pack()
Button(root, text="open 2nd window", command=openwind).pack()


root.mainloop()



