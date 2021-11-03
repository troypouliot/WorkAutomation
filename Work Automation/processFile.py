import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import os

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

#Logo
logo = Image.open('Minco Logo.jpg')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#Instructions
instructions = tk.Label(root, text='Select a file to open', font='Arial', pady=10)
instructions.grid(columnspan=3, column=0, row=1)

def openfile():
    browseText.set('Loading...')
    myfile = askopenfile(parent=root, mode='r', title="Choose a file", filetype=[("EX2 File", "*.ex2")])
    if myfile:
        #Text box
        textbox = tk.Text(root, height=10, width=50, padx=15,pady=15)
        textbox.insert(1.0, myfile.readlines())
        textbox.grid(column=1, row=3)
        browseText.set('Browse')
        # filepath = tk.Label(root, text=fp)
        # filepath.grid(columnspan=3, column=0, row=3)



#browse button
browseText = tk.StringVar()
browseBtn = tk.Button(root, textvariable=browseText, command=lambda: openfile(), font='Arial', bg='#20bebe', fg='white', height=2, width=50)
browseText.set('Browse')
browseBtn.grid(column=1, row=2)

canvas = tk.Canvas(root, width=600, height=250)
canvas.grid(columnspan=3)

root.mainloop()

