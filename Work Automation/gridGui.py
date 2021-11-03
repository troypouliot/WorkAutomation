from tkinter import *

root = Tk()
root.configure(bg="yellow")
root.geometry("400x400")

# # Create label widget
# myLabel1 = Label(root, text='Hello World', width=100)
# myLabel2 = Label(root, text='My name is Troy')
#
# # Shoving it onto the screen
# myLabel1.grid(row=0, column=0)
# myLabel2.grid(row=1, column=1)

slider_frame = Frame(root, borderwidth=5, relief=SUNKEN)
slider_frame.pack(pady=10)

def calculate_total_bill(value):
    print(value)
    if slider.get()!=' ':
        tip_percent=float(value)
        bill=float(slider.get())
        tip_amount=tip_percent*bill
        text=f'(bill+tip_amount)'
        slider.configure(text=text)

slider = Scale(slider_frame, from_=0.00, to=1.0,orient=HORIZONTAL, length=400, tickinterval=0.1, resolution=0.01, command=calculate_total_bill)
slider.pack()
root.mainloop()



