from tkinter import *

root = Tk()
root.title('Frames')

# Create label widget
myLabel = Label(root, text='Hello World')

frame = LabelFrame(root, padx=50, pady=50)
frame.pack(padx=100, pady=100)

button = Button(frame, text="Button")
button2 = Button(frame, text="Button2")
button.grid(row=0, column=0)
button2.grid(row=1, column=1)

# Shoving it onto the screen
myLabel.pack()


root.mainloop()



