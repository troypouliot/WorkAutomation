import re
import os


def instructionBlock(text):
    textlen = len(text)
    sdf = int((78 - textlen) / 2)
    print(('*' * sdf) + ' ' + text + ' ' + ('*' * sdf))


########################################################################
#   This program converts the gcode format output by the Genflex Schmoll
#   automation into something readable by a gcode simulator such as the
#   one found here - https://gcodetutor.com/cnc-program-simulator.html
########################################################################

instructionBlock('The input file must be located here-')
instructionBlock(r'C:\Users\troypouliot\Google Drive\Programming Training\Work Automation')

fileName = ''
while ''.join(fileName) != '0':
    print('What is the file name?')
    fileName = input('Enter 0 to quit: ').split('.')
    if fileName == 0:
        quit()
    elif os.path.isfile(r'C:\Users\troypouliot\Google Drive\Programming Training\Work Automation\{}'
                              .format('.'.join(fileName))):

        inputFile = open(r'C:\Users\troypouliot\Google Drive\Programming Training\Work Automation\{}'
                         .format('.'.join(fileName)), 'r')
        outputFile = open(r'C:\Users\troypouliot\Google Drive\Programming Training\Work Automation\{}'
                          .format(fileName[0] + '_edit' + '.ex2'), 'w')
        g01Regex = re.compile(r'G01X\d\d')
        g00Regex = re.compile(r'G00X\d\d')
        xRegex3 = re.compile(r'^X\d\d')
        g02Regex = re.compile(r'G02X\d\d')
        g03Regex = re.compile(r'G03X\d\d')
        m12Regex = re.compile(r'M12')
        m11Regex = re.compile(r'M11')
        m01Regex = re.compile(r'M01')
        m25Regex = re.compile(r'M25')
        g05Regex = re.compile(r'G05')
        g40Regex = re.compile(r'G40')
        m15Regex = re.compile(r'M15')
        m17Regex = re.compile(r'M17')
        m08Regex = re.compile(r'M08')

        inputList = inputFile.readlines()
        inputFile.close()
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
                edit = '{}.{}.{}R{}.{}   ;CIRCULAR CW MOVE{}'\
                    .format(mo[:6], mo[6:13], mo[13:17], mo[18:20], mo[20:24], '\n')
                # edit = mo[:6] + '.' + mo[6:13] + '.' + mo[13:17] + 'R' + mo[18:20] + '.' + mo[20:24] + '   ;CIRCULAR CW MOVE' + '\n'
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
                edit = mo[:3] + '                           ;DRILL MODE (SKIVE)' + '\n'
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
            else:
                newList.append(mo)
        outputFile.write(''.join(newList))
        outputFile.close()
        break
    else:
        print('That file does not exist, try again. Enter 0 to exit.')
