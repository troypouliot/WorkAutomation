import os
from win32com.client import Dispatch


path = os.path.abspath(r"J:\genesis\fw\jobs\237866\output\237866_.lnk") # location and name of the shortcut (must include .lnk)
target = r"F:\Parts\237000\237866HAP\3-Design\304-CADCAM\237866" # what do you want the shortcut to open (file, folder?
# wDir = r"P:\Media\Media Player Classic"
# icon = r"P:\Media\Media Player Classic\mplayerc.exe"
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
# shortcut.WorkingDirectory = wDir
# shortcut.IconLocation = icon
shortcut.save()

# def createShortcut(path, target='', wdir='', icon=''):
#     ext = path[-3:]
#     if ext == 'url':
#         shortcut = file(path, 'w')
#         shortcut.write('[InternetShortcut]\n')
#         shortcut.write('URL=%s' % target)
#         shortcut.close()
#     else:
#         shell = Dispatch('WScript.Shell')
#         shortcut = shell.CreateShortCut(path)
#         shortcut.Targetpath = target
#         shortcut.WorkingDirectory = wdir
#         if icon == '':
#             pass
#         else:
#             shortcut.IconLocation = icon
#         shortcut.save()
#
#
# create_lnk(r'J:\genesis\fw\jobs\237962\output\237962-1b2.d.lst', r'J:\genesis\fw\jobs\237962\output\\')
#
#



