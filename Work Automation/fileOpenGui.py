from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import re

root = Tk()

root.iconbitmap('Minco_M.ico')
root.title('Verify .ex2 file')

# Create label widget

myLogo = ImageTk.PhotoImage(Image.open('Minco Logo.png'))
logoLabel = Label(image=myLogo)

def loadFile():
    global fileName, input_file_label
    fileName = filedialog.askopenfilename(initialdir="/", title='Open a file', filetypes=[("Schmoll Files", "*.ex2")])
    filename_str.set('File Loaded: ' + fileName)


def doThing():
    try:
        if str(fileName).endswith('.ex2'):
            with open(fileName, 'r') as schmoll_file:
                lines = schmoll_file.readlines()
            print(lines)
            m12Regex = re.compile(r'M12')
            m12_count = 0
            for line in lines:
                if m12Regex.match(line):
                    m12_count += 1
            if m12_count == 0:
                messagebox.showwarning('Warning', 'No "M12" lines found')
                file_contents = Text(root, width=100, height=10)
                file_contents.grid(row=5, columnspan=3)
                file_contents.insert(INSERT, str(lines))
            else:
                messagebox.showinfo('Yay!', 'Found {} targeted subgroups'.format(m12_count))
                file_contents = Text(root, width=100, height=10)
                file_contents.grid(row=5, columnspan=3)
                file_contents.insert(INSERT, lines)
        else:
            messagebox.showinfo("INFO", "Please load a file first")
    except NameError:
        messagebox.showinfo("INFO", "Please load a file first")


filename_str = StringVar()
filename_str.set('')
input_file_label = Label(root, textvariable=filename_str).grid(row=4, column=0, columnspan=3)
instLabel = Label(root, text="Click the button below to open a file")
openButton = Button(root, text='Load File', command=loadFile)
runButton = Button(root, text="Check Program", command=doThing)

logoLabel.grid(row=0, column=0, columnspan=3)
instLabel.grid(row=1, column=0, columnspan=3, padx=20, pady=20)
openButton.grid(row=2, column=0, columnspan=3, pady=20, padx=5)
runButton.grid(row=2, column=2, pady=20, padx=5)
root.mainloop()

