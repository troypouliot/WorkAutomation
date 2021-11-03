from tkinter import *
from PIL import ImageTk, Image

root = Tk()



# Create label widget

root.iconbitmap('car.ico')
root.title('Image Viewer')

my_img1 = ImageTk.PhotoImage(Image.open('images/img1.jpg'))
my_img2 = ImageTk.PhotoImage(Image.open('images/img2.jpg'))
my_img3 = ImageTk.PhotoImage(Image.open('images/img3.jpg'))
my_img4 = ImageTk.PhotoImage(Image.open('images/img4.jpg'))
my_img5 = ImageTk.PhotoImage(Image.open('images/img5.jpg'))

img_list = [my_img1, my_img2, my_img3, my_img4, my_img5]

status = Label(root, text='Image {} of {}'.format('1', len(img_list)), bd=1, relief=SUNKEN, anchor=E, pady=2, padx=2)

my_label = Label(image=img_list[0])
my_label.grid(row=0, column=0, columnspan=3)



def forward(index):
    global my_label, button_forward, button_back, status
    my_label.grid_forget()
    status.grid_forget()
    my_label = Label(image=img_list[index - 1])
    button_forward = Button(root, text='-->', padx=10, command=lambda: forward(index + 1))
    button_back = Button(root, text='<--', padx=10, command=lambda: back(index - 1))

    if index == 5:
        button_forward = Button(root, text='-->', padx=10, state=DISABLED)
    status = Label(root, text='Image {} of {}'.format(index, len(img_list)), bd=1, relief=SUNKEN, anchor=E, pady=2, padx=2)
    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)


def back(index):
    global my_label, button_forward, button_back, status
    my_label.grid_forget()
    status.grid_forget()
    my_label = Label(image=img_list[index - 1])
    button_forward = Button(root, text='-->', padx=10, command=lambda: forward(index + 1))
    button_back = Button(root, text='<--', padx=10, command=lambda: back(index - 1))

    if index == 1:
        button_back = Button(root, text='<--', padx=10, state=DISABLED)
    status = Label(root, text='Image {} of {}'.format(index, len(img_list)), bd=1, relief=SUNKEN, anchor=E, pady=2, padx=2)
    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)


button_back = Button(root, text='<--', padx=10, state=DISABLED, command=back)
button_forward = Button(root, text='-->', padx=10, command=lambda: forward(2))
button_quit = Button(root, text='Exit', padx=10, command=root.quit)

button_back.grid(row=1, column=0)
button_forward.grid(row=1, column=2)
button_quit.grid(row=1, column=1, pady=10)
status.grid(row=2, column=0, columnspan=3, sticky=W+E)

root.mainloop()



