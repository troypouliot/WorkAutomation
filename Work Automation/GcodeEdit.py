import re
import os
import sys


file = sys.argv[1]
# file = 'rex.gcode'
out_file = 'edit_{}'.format(file)
remove_tool_num = re.compile(r'(M10\d S\d\d\d) (T\d+)( ;[\w\s]+$)')
single_tool_number = re.compile(r'^T\d')
first_m600 = re.compile(r'^M600')
fileName = ''

m600_count = 0
with open(file, 'r') as inputFile:
    inputList = inputFile.readlines()

destFile = re.sub('\.gcode$', '', file)
os.rename(file, destFile + '.bak')
destFile = re.sub('\.gcode$', '', file)
destFile = destFile + '.gcode'

with open(destFile, 'w') as outputFile:
    for mo in inputList:
        if remove_tool_num.search(mo):
            outputFile.write(re.sub(remove_tool_num, '\g<1>\g<3>', mo))
        elif single_tool_number.search(mo):
            continue
        elif first_m600.search(mo):
            if m600_count < 1:
                m600_count = 1
                continue
            else:
                outputFile.write(mo)
        else:
            outputFile.write(mo)

