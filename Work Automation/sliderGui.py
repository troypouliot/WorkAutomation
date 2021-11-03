from tkinter import *

root = Tk()
root.title("Main Window")
root.geometry("400x400")

vertical = Scale(root, from_=0, to=1000, showvalue='yes')
vertical.pack(anchor=E)

horizontal = Scale(root, from_=0, to=1000, orient=HORIZONTAL)
horizontal.pack()


def slide():
    my_label = Label(root, text=horizontal.get()).pack()
    root.geometry(str(horizontal.get()) + "x" + str(vertical.get()))


my_btn = Button(root, text="click me", command=slide).pack()

root.mainloop()



