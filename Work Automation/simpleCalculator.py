from tkinter import *

root = Tk()
root.title("Calculator")


display = Entry(root, width=35, borderwidth=5)
display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


def button_click(number):
    current = display.get()
    display.delete(0, END)
    display.insert(0, str(current) + str(number))

def button_clear():
    display.delete(0, END)

def button_add():
    global x, operator
    x = int(display.get())
    display.delete(0, END)
    operator = "addition"

def button_sub():
    global x, operator
    x = int(display.get())
    display.delete(0, END)
    operator = "subtraction"

def button_mult():
    global x, operator
    x = int(display.get())
    display.delete(0, END)
    operator = "multiplication"

def button_div():
    global x, operator
    x = int(display.get())
    display.delete(0, END)
    operator = "division"


def button_equal():
    y = int(display.get())
    display.delete(0, END)
    if operator == 'addition':
        display.insert(0, x + y)
    if operator == 'subtraction':
        display.insert(0, x - y)
    if operator == 'multiplication':
        display.insert(0, x * y)
    if operator == 'division':
        display.insert(0, x / y)



button_1 = Button(root, text='1', padx=40, pady=20, command=lambda: button_click(1))
button_2 = Button(root, text='2', padx=40, pady=20, command=lambda: button_click(2))
button_3 = Button(root, text='3', padx=40, pady=20, command=lambda: button_click(3))
button_4 = Button(root, text='4', padx=40, pady=20, command=lambda: button_click(4))
button_5 = Button(root, text='5', padx=40, pady=20, command=lambda: button_click(5))
button_6 = Button(root, text='6', padx=40, pady=20, command=lambda: button_click(6))
button_7 = Button(root, text='7', padx=40, pady=20, command=lambda: button_click(7))
button_8 = Button(root, text='8', padx=40, pady=20, command=lambda: button_click(8))
button_9 = Button(root, text='9', padx=40, pady=20, command=lambda: button_click(9))
button_0 = Button(root, text='0', padx=40, pady=20, command=lambda: button_click(0))
button_add = Button(root, text='+', padx=39, pady=20, command=button_add)
button_sub = Button(root, text='-', padx=40, pady=20, command=button_sub)
button_mult = Button(root, text='*', padx=40, pady=20, command=button_mult)
button_div = Button(root, text='/', padx=39, pady=20, command=button_div)
button_equal = Button(root, text='=', padx=91, pady=20, command=button_equal)
button_clear = Button(root, text='Clear', padx=29, pady=20, command=button_clear)

button_7.grid(column=0, row=1)
button_8.grid(column=1, row=1)
button_9.grid(column=2, row=1)

button_4.grid(column=0, row=2)
button_5.grid(column=1, row=2)
button_6.grid(column=2, row=2)

button_1.grid(column=0, row=3)
button_2.grid(column=1, row=3)
button_3.grid(column=2, row=3)

button_0.grid(row=4, column=0)
button_clear.grid(row=4, column=2)
button_add.grid(row=4, column=1)
button_sub.grid(row=5, column=0)
button_mult.grid(row=5, column=1)
button_div.grid(row=5, column=2)
button_equal.grid(row=6, column=0, columnspan=3)




root.mainloop()



