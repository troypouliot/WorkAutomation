from tkinter import *
from tkinter import filedialog, messagebox
from os import path
from re import compile
from webbrowser import open as wopen

root = Tk()
root.title('Format .ex2 file')



def openbrowser():
    wopen('https://gcodetutor.com/cnc-program-simulator.html')


def loadFile():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="/", title='Select a .ex2 file', filetypes=[("Schmoll Files", "*.ex2")])
    input_file_str.set('File Loaded: ' + fileName)


def doThing():
    global fileName
    try:
        if str(fileName).endswith('.ex2'):
            #   Regular expressions
            g01Regex = compile(r'G01X\d\d')
            g00Regex = compile(r'G00X\d\d')
            xRegex3 = compile(r'^X\d\d')
            g02Regex = compile(r'G02X\d\d')
            g03Regex = compile(r'G03X\d\d')
            m12Regex = compile(r'M12')
            m11Regex = compile(r'M11')
            m01Regex = compile(r'M01')
            m25Regex = compile(r'M25')
            g05Regex = compile(r'G05')
            g40Regex = compile(r'G40')
            m15Regex = compile(r'M15')
            m17Regex = compile(r'M17')
            m08Regex = compile(r'M08')
            toolRegex = compile(r'^T\d\n')

            #   Open the selected file, read contents, and close
            edit_file = open(fileName, 'r')
            inputList = edit_file.readlines()
            edit_file.close()

            toolList = ''

            for tool in inputList[:31]:
                if (tool.startswith('T')) and (len(tool) > 3):
                    toolList += tool
            newtoollist = toolList.split('\n')

            tool_dict = {}
            i = 1
            for t in newtoollist:
                if t.startswith('T'):
                    tool_dict['T{}'.format(i)] = t
                    i += 1

            newList = []
            for mo in inputList:
                if g01Regex.search(mo):
                    edit = mo[:6] + '.' + mo[6:13] + '.' + mo[13:17] + '           ;ROUT CUT' + '\n'
                    newList.append(edit)
                elif g00Regex.search(mo):
                    edit = mo[:6] + '.' + mo[6:13] + '.' + mo[13:17] + '           ;TRAVEL MOVE' + '\n'
                    newList.append(edit)
                elif xRegex3.search(mo):
                    edit = mo[:3] + '.' + mo[3:10] + '.' + mo[10:]
                    newList.append(edit)
                elif g02Regex.search(mo):
                    edit = '{}.{}.{}R{}.{}   ;CIRCULAR CW MOVE{}' \
                        .format(mo[:6], mo[6:13], mo[13:17], mo[18:20], mo[20:24], '\n')
                    newList.append(edit)
                elif g03Regex.search(mo):
                    edit = mo[:6] + '.' + mo[6:13] + '.' + mo[13:17] + 'R' + mo[18:20] + '.' + mo[20:24] + '   ;CIRCULAR CCW MOVE' + '\n'
                    newList.append(edit)
                elif m11Regex.search(mo):
                    edit = mo[:3] + '                           ;GLOBAL TARGETS' + '\n'
                    newList.append(edit)
                elif m12Regex.search(mo):
                    edit = mo[:3] + '                           ;SUBGROUP TARGETS' + '\n'
                    newList.append(edit)
                elif m01Regex.search(mo):
                    edit = mo[:3] + '                           ;END OF PATTERN' + '\n'
                    newList.append(edit)
                elif m25Regex.search(mo):
                    edit = mo[:3] + '                           ;BEGINNING OF STEP AND REPEAT' + '\n'
                    newList.append(edit)
                elif m08Regex.search(mo):
                    edit = mo[:3] + '                           ;END OF STEP AND REPEAT' + '\n'
                    newList.append(edit)
                elif g05Regex.search(mo):
                    edit = mo[:3] + '                           ;DRILL MODE' + '\n'
                    newList.append(edit)
                elif g40Regex.search(mo):
                    edit = mo[:3] + '                           ;CUTTER COMP OFF' + '\n'
                    newList.append(edit)
                elif m15Regex.search(mo):
                    edit = mo[:3] + '                           ;HEAD DOWN' + '\n'
                    newList.append(edit)
                elif m17Regex.search(mo):
                    edit = mo[:3] + '                           ;HEAD UP' + '\n'
                    newList.append(edit)
                elif toolRegex.search(mo):
                    edit = mo[:2] + '                            ;' + tool_dict[mo[:2]] + '\n'
                    newList.append(edit)
                else:
                    newList.append(mo)
            out_file_name = path.basename(fileName).split('.')[0] + '_edited.ex2'
            outputFile = open(path.dirname(fileName) + '/' + out_file_name, 'w')
            outputFile.write(''.join(newList))
            outputFile.close()

            output_file_str.set('Output as: ' + out_file_name)

    except NameError:
        messagebox.showinfo("INFO", "Please load a file first")


#   Buttons
openButton = Button(root, text='Load File', command=loadFile).grid(row=2, column=0, columnspan=1,padx=5, pady=10, ipadx=9, sticky=W)
runButton = Button(root, text='Output .ex2', command=doThing).grid(row=3, column=0, pady=10, padx=5, sticky=W)
openBrowser = Button(root, text='Open G code simulator website', command=openbrowser).grid(row=4, column=0, columnspan=2, sticky=W, padx=5, pady=10)

#   Labels
input_file_str = StringVar()
input_file_str.set('')
input_file_label = Label(root, textvariable=input_file_str).grid(row=2, column=1, columnspan=3, sticky=W)
output_file_str = StringVar()
output_file_str.set('')
output_file_label = Label(root, textvariable=output_file_str).grid(row=3, column=1, columnspan=3, sticky=W)
versionLabel = Label(root, text='Version 0.2.0', relief='sunken').grid(row=5,column=5, columnspan=6, sticky=EW)


root.mainloop()

