import os
import openpyxl

partPrefix = input('What model prefix are you looking for? ').upper()
partsList = []
for folderName, subfolders, filenames in os.walk(r'F:\Parts\\'):
    for sub in subfolders:
        for folderName1, subfolders1, filenames1 in os.walk('F:\\Parts\\' + sub):
            for sub1 in subfolders1:
                if sub1.endswith(partPrefix):
                    partsList.append(str(sub1))
            break
    break
print(*partsList, sep='\n')
print('Found {} models with the prefix {}'.format(len(partsList), partPrefix))
