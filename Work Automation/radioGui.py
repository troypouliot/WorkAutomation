from tkinter import *

root = Tk()
root.title("Radio Buttons")

# r = IntVar()
# r.set(2)

modes = [
    ("Pepperoni", "Pepperoni"),
    ("Cheese", "Cheese"),
    ("Sausage", "Sausage"),
    ("Veggie", "Veggie"),
]

pizza = StringVar()
pizza.set("Cheese")
myLabel = Label(root, text=pizza.get()).pack()
for text, mode in modes:
    Radiobutton(root, text=text, variable=pizza, value=mode).pack(anchor=W)


def click(value):
    global myLabel
    myLabel.destroy()
    myLabel = Label(root, text=value).pack()

# Radiobutton(root, text="Option 1", variable=r, value=1, command=lambda: click(r.get())).pack()
# Radiobutton(root, text="Option 2", variable=r, value=2, command=lambda: click(r.get())).pack()

# myLabel = Label(root, text=pizza.get()).pack()


myButton = Button(root, text='Click me', command=lambda: click(pizza.get())).pack()

root.mainloop()



