import ctypes
import os
import shelve

check_file = os.path.abspath(r'F:\HEATERS\Production\Marking\MarkingStamps\MARKINGSTAMPORDER.xlsm')
file_mod_time = os.path.getmtime(check_file)


with shelve.open(r'C:\Users\troypouliot\Google Drive\Programming Training\Python\Work Automation\CheckMarkingStamp\filedate') as fd:
    date = fd['modified_date']
    if date < os.path.getmtime(check_file):
        ctypes.windll.user32.MessageBoxW(0, 'Marking stamp file has been updated', 'Stamp File Updated')
        fd['modified_date'] = os.path.getmtime(check_file)




