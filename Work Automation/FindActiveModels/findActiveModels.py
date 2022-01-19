from os import path, listdir, walk
import PySimpleGUI as sg
import threading

F_DRIVE = 'F:\\Parts\\'.lower()
I_DRIVE = 'I:\\US\\Parts\\'.lower()
OLD_F_LOC = 'F:\\HEATERS\\Eng\\Parts\\'.lower()
OLD_I_LOC = 'I:\\US\\Heaters\\Eng\\Parts\\'.lower()
TREE_1 = ['3-Design'.lower(), '3_Design'.lower(), 'CAD'.lower()]
TREE_2 = ['304-CADCAM'.lower(), '304_CADCAM'.lower()]


def countFiles(dir_path):
    return len([name for name in listdir(dir_path) if path.isfile(path.join(dir_path, name))]) - 1


def isActive(dir_path, prefix, model_num):
    try:
        all_files = [name for name in listdir(dir_path) if path.isfile(path.join(dir_path, name))]
    except FileNotFoundError:
        return 'NA'
    key_files = []
    pre = []
    if countFiles(dir_path) > 4:
        for file in all_files:
            if model_num.strip(prefix) in file:
                key_files.append(file.split(model_num)[0])
        for _ in key_files:
            if len(_) > 1:
                pre.append(_.upper())
        if len(pre) > 0:
            winner = max(set(pre), key=pre.count), model_num
            return [winner[0], winner[1]]
        else:
            return 'NA'
    else:
        return 'NA'


def check4CADFiles(dir_path):
    cad_file_ext = ['.M', '.CAD', '.M1', '.M2', '.M3', '.STP']
    f_count = 0
    for ext in cad_file_ext:
        if cnt := len(
                [name for name in listdir(dir_path) if path.splitext(path.join(dir_path, name))[1].upper() == ext]):
            f_count += cnt
    if f_count > 0:
        return True
    return False


def emptyprefix():
    window['-MLINE_KEY-'].update('Please enter a model prefix to search.\n', append=True)
    return


def find_cur_f_loc(pre=''):
    if pre == '':
        emptyprefix()
    else:
        window['-stop-'].update(visible=True)
        window['-MLINE_KEY-'].update('Searching the {} location...\n'.format(F_DRIVE.upper()), append=True)
        partPrefix = pre.upper()
        partcount = 0
        for folderName, subfolders, filenames in walk(F_DRIVE):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(F_DRIVE, sub)):
                    for sub1 in subfolders1:
                        if sub1.endswith(partPrefix):
                            modelpath = path.join(F_DRIVE, sub, sub1)
                            for tree1 in TREE_1:
                                if path.exists(path.normcase(path.join(modelpath, tree1))):
                                    for tree2 in TREE_2:
                                        if path.exists(path.join(modelpath, tree1, tree2)):
                                            if path.exists(
                                                    path.join(modelpath, tree1, tree2, sub1.strip(partPrefix))):
                                                partcount += 1
                                                # print(partPrefix, sub1.split(partPrefix)[0])
                                                window['-MLINE_KEY-'].update('{}\n'.format(partPrefix + ' ' + sub1.split(partPrefix)[0]), append=True)
                    break
            break
        window['-MLINE_KEY-'].update('DONE! \nFound {} active "{}" models. in the "{}" location.\n'.format(partcount, partPrefix, F_DRIVE.upper()), append=True)
        window['-stop-'].update(visible=False)


def find_old_f_loc(pre=''):
    if pre == '':
        emptyprefix()
    else:
        window['-stop-'].update(visible=True)
        window['-MLINE_KEY-'].update('Searching the {} location...\n'.format(OLD_F_LOC.upper()), append=True)
        pre = pre.upper()
        model_list = []
        for folderName, subfolders, filenames in walk(OLD_F_LOC):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
                    for sub1 in subfolders1:
                        modelpath = path.normcase(path.join(folderName, sub, sub1))
                        if check4CADFiles(modelpath) is True:
                            model_list.append(isActive(path.join(folderName, sub, sub1), '', sub1))
                            if pre == '':
                                continue
                            if model_list[-1][0] != pre:
                                model_list.pop()
                            else:
                                window['-MLINE_KEY-'].update('{}\n'.format(model_list[-1][0] + ' ' + model_list[-1][1]), append=True)
                            continue
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                    model_list.append(isActive(path.join(folderName, sub, sub1, tree1), '', sub1))
                                    if pre == '':
                                        continue
                                    if model_list[-1][0] != pre:
                                        model_list.pop()
                                    else:
                                        window['-MLINE_KEY-'].update('{}\n'.format(model_list[-1][0] + ' ' + model_list[-1][1]), append=True)
                                    continue
                                TREE_2.append(sub1)
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                                            model_list.append(
                                                isActive(path.join(folderName, sub, sub1, tree1, tree2), '', sub1))
                                            if pre == '':
                                                continue
                                            if model_list[-1][0] != pre:
                                                model_list.pop()
                                            else:
                                                window['-MLINE_KEY-'].update('{}\n'.format(model_list[-1][0] + ' ' + model_list[-1][1]), append=True)
                                TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                    break
            break
        window['-MLINE_KEY-'].update('DONE! \nFound {} active "{}" models. in the "{}" location.\n'.format(len(model_list), pre, OLD_F_LOC.upper()), append=True)
        window['-stop-'].update(visible=False)


def find_cur_i_loc(pre=''):
    if pre == '':
        emptyprefix()
    else:
        window['-stop-'].update(visible=True)
        window['-MLINE_KEY-'].update('Searching the {} location...\n'.format(I_DRIVE.upper()), append=True)
        partPrefix = pre.upper()
        partcount = 0
        for folderName, subfolders, filenames in walk(I_DRIVE):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(I_DRIVE, sub)):
                    for sub1 in subfolders1:
                        if sub1.endswith(partPrefix):
                            modelpath = path.join(I_DRIVE, sub, sub1)
                            for tree1 in TREE_1:
                                if path.exists(path.normcase(path.join(modelpath, tree1))):
                                    for tree2 in TREE_2:
                                        if path.exists(path.join(modelpath, tree1, tree2)):
                                            if path.exists(
                                                    path.join(modelpath, tree1, tree2, sub1.strip(partPrefix))):
                                                # print(partPrefix, sub1.split(partPrefix)[0])
                                                partcount += 1
                                                window['-MLINE_KEY-'].update('{}\n'.format(partPrefix + ' ' + sub1.split(partPrefix)[0]), append=True)
                    break
            break
        window['-MLINE_KEY-'].update('DONE! \nFound {} active "{}" models. in the "{}" location.\n'.format(partcount, partPrefix, I_DRIVE.upper()), append=True)
        window['-stop-'].update(visible=False)


def find_old_i_loc(pre=''):
    if pre == '':
        emptyprefix()
    else:
        window['-stop-'].update(visible=True)
        window['-MLINE_KEY-'].update('Searching the {} location...\n'.format(OLD_I_LOC.upper()), append=True)
        pre = pre.upper()
        model_list = []
        for folderName, subfolders, filenames in walk(OLD_I_LOC):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
                    for sub1 in subfolders1:
                        modelpath = path.normcase(path.join(folderName, sub, sub1))
                        if check4CADFiles(modelpath) is True:
                            model_list.append(isActive(path.join(folderName, sub, sub1), '', sub1))
                            if pre == '':
                                continue
                            if model_list[-1][0] != pre:
                                model_list.pop()
                            else:
                                window['-MLINE_KEY-'].update('{}\n'.format(model_list[-1][0] + ' ' + model_list[-1][1]), append=True)
                            continue
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                    model_list.append(isActive(path.join(folderName, sub, sub1, tree1), '', sub1))
                                    if pre == '':
                                        continue
                                    if model_list[-1][0] != pre:
                                        model_list.pop()
                                    else:
                                        window['-MLINE_KEY-'].update('{}\n'.format(model_list[-1][0] + ' ' + model_list[-1][1]), append=True)
                                    continue
                                TREE_2.append(sub1)
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                                            model_list.append(
                                                isActive(path.join(folderName, sub, sub1, tree1, tree2), '', sub1))
                                            if pre == '':
                                                continue
                                            if model_list[-1][0] != pre:
                                                model_list.pop()
                                            else:
                                                window['-MLINE_KEY-'].update('{}\n'.format(model_list[-1][0] + ' ' + model_list[-1][1]), append=True)
                                TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                    break
            break
        window['-MLINE_KEY-'].update('DONE! \nFound {} active "{}" models. in the "{}" location.\n'.format(len(model_list), pre, OLD_I_LOC.upper()), append=True)
        window['-stop-'].update(visible=False)




layout = [  [sg.Text('Model prefix to search for:'), sg.Input(key='-prefix-', size=(5))],
            [sg.Button('Search Current F Drive', key='-search_cur_f-'), sg.Button('Search Current I Drive', key='-search_cur_i-'),
             sg.Button('Search Old F Drive', key='-search_old_f-'), sg.Button('Search Old I Drive', key='-search_old_i-')],
            [sg.Text('Search Results:', font='Any 18'), sg.Button('Stop Search', key='-stop-', visible=False, button_color=('black', 'red'))],
            [sg.Multiline(size=(80,20), key='-MLINE_KEY-', write_only=True, auto_refresh=True, autoscroll=True, disabled=True)],
            [sg.Button('Quit', key='-quit-')]]

window = sg.Window('Minco Active Model Finder', layout)


while True:
    event, values = window.read(timeout=500)
    print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit', '-quit-'):
        break
    elif event == '-search_cur_f-':
        find_cur_f_loc(window['-prefix-'].get())
    elif event == '-search_cur_i-':
        find_cur_i_loc(window['-prefix-'].get())
    elif event == '-search_old_f-':
        find_old_f_loc(window['-prefix-'].get())
    elif event == '-search_old_i-':
        find_old_i_loc(window['-prefix-'].get())
    elif event == '-stop-':
        pass

window.close()

