from tkinter import *
from PIL import ImageTk, Image

root = Tk()


# Create label widget
myLabel = Label(root, text='Hello World')
root.iconbitmap('car.ico')

my_img = ImageTk.PhotoImage(Image.open('IMG_4390.JPG'))
my_label = Label(image=my_img)
my_label.pack()

# Shoving it onto the screen
myLabel.pack()

button_quit = Button(root, text="Exit Program", command=root.quit)
button_quit.pack()


root.mainloop()



