from os import path, listdir, walk
import PySimpleGUI as sg
import pickle
import time
import threading
import pprint


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
            return winner[0], winner[1]
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


def save_db(data):

    try:
        if stop_index:
            raise StopIteration
        with open('.\\db\\active_parts', 'wb') as db:
            pickle.dump(data, db)
    except StopIteration:
        pass


def read_db():
    try:
        with open('.\\db\\active_parts', 'rb') as db:
            return pickle.load(db)
    except FileNotFoundError:
        blank_dict = {'DB Date': 'N/A', 'Models': []}
        with open('.\\db\\active_parts', 'wb') as db:
            pickle.dump(blank_dict, db)


def write_to_dict(prefix, model):
    global partsdict
    partsdict['DB Date'] = time.strftime('%Y-%m-%d %I:%M%p', time.localtime())
    try:
        partsdict['Models'].append((prefix, int(model)))
    except ValueError:
        pass
    return partsdict


def find_cur_f_loc():
    try:
        for folderName, subfolders, filenames in walk(F_DRIVE):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(F_DRIVE, sub)):
                    for sub1 in subfolders1:
                        if stop_index:
                            raise StopIteration
                        modelpath = path.join(F_DRIVE, sub, sub1)
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if path.exists(path.join(modelpath, tree1, tree2, sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                            write_to_dict(sub1.strip('1234567890'), sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                                            window['-MLINE_KEY-'].write(sub1.strip('1234567890') + sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + '\n')
                                            if stop_index:
                                                raise StopIteration
                    break
            break
    except StopIteration:
        pass


def find_old_f_loc():
    try:
        for folderName, subfolders, filenames in walk(OLD_F_LOC):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
                    for sub1 in subfolders1:
                        if stop_index:
                            raise StopIteration
                        modelpath = path.normcase(path.join(folderName, sub, sub1))
                        if check4CADFiles(modelpath) is True:
                            pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                            if pre != 'N' and len(pre) <= 5:
                                write_to_dict(pre, model)
                                window['-MLINE_KEY-'].write(pre + model + '\n')
                                if stop_index:
                                    raise StopIteration
                            continue
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                    pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                                    if pre != 'N' and len(pre) <= 5:
                                        write_to_dict(pre, model)
                                        window['-MLINE_KEY-'].write(pre + model + '\n')
                                        if stop_index:
                                            raise StopIteration
                                    continue
                                TREE_2.append(sub1)
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                                            pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                                            if pre != 'N' and len(pre) <= 5:
                                                write_to_dict(pre, model)
                                                window['-MLINE_KEY-'].write(pre + model + '\n')
                                                if stop_index:
                                                    raise StopIteration
                                TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                    break
            break
    except StopIteration:
        pass


def find_cur_i_loc():
    try:
        for folderName, subfolders, filenames in walk(I_DRIVE):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(I_DRIVE, sub)):
                    for sub1 in subfolders1:
                        if stop_index:
                            raise StopIteration
                        modelpath = path.join(I_DRIVE, sub, sub1)
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if path.exists(
                                                path.join(modelpath, tree1, tree2, sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                            write_to_dict(sub1.strip('1234567890'), sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                                            window['-MLINE_KEY-'].write(sub1.strip('1234567890') + sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + '\n')
                                            if stop_index:
                                                raise StopIteration

                    break
            break
    except StopIteration:
        pass


def find_old_i_loc():
    try:
        for folderName, subfolders, filenames in walk(OLD_I_LOC):
            for sub in subfolders:
                for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
                    for sub1 in subfolders1:
                        if stop_index:
                            raise StopIteration
                        modelpath = path.normcase(path.join(folderName, sub, sub1))
                        if check4CADFiles(modelpath) is True:
                            pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                            if pre != 'N' and len(pre) <= 5:
                                write_to_dict(pre, model)
                                window['-MLINE_KEY-'].write(pre + model + '\n')
                            if stop_index:
                                raise StopIteration
                            continue
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                    pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                                    if pre != 'N' and len(pre) <= 5:
                                        write_to_dict(pre, model)
                                        window['-MLINE_KEY-'].write(pre + model + '\n')
                                    if stop_index:
                                        raise StopIteration
                                    continue
                                TREE_2.append(sub1)
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                                            pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                                            if pre != 'N' and len(pre) <= 5:
                                                write_to_dict(pre, model)
                                                window['-MLINE_KEY-'].write(pre + model + '\n')
                                            if stop_index:
                                                raise StopIteration
                                TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                    break
            break
    except StopIteration:
        pass


def reindex_thread(window):
    global partsdict
    partsdict['DB Date'] = 'NA'
    partsdict['Models'] = []
    window['-progress-'].update(0, 100, visible=True)
    find_cur_f_loc()
    window['-progress-'].update(25, 100)
    find_cur_i_loc()
    window['-progress-'].update(50, 100)
    find_old_i_loc()
    window['-progress-'].update(75, 100)
    find_old_f_loc()
    window['-progress-'].update(99, 100)
    save_db(partsdict)
    window['-progress-'].update(100, 100, visible=False)
    window['-db_date-'].update('Last database index: {}'.format(read_db()['DB Date']))
    window.write_event_value('-Indexing Done-', '')


def reindex():
    threading.Thread(target=reindex_thread, args=(window,), daemon=True).start()


def show_all_thread(window):
    filtered_list = []
    for model in partsdict['Models']:
        filtered_list.append(model)
        if stop_index:
            break
    filtered_list.sort(key=lambda x:x[1])

    for model in filtered_list:
        window['-MLINE_KEY-'].write(model[0] + str(model[1]) + '\n')
        if stop_index:
            break
    window['-loading-'].update(visible=False)
    window.write_event_value('-Indexing Done-', '')


def show_all():
    threading.Thread(target=show_all_thread, args=(window,), daemon=True).start()

def prefix_thread(window):
    window['-MLINE_KEY-'].update('')
    filtered_list = []
    for model in partsdict['Models']:
        if model[0] == window['-prefix-'].get().upper():
            filtered_list.append(model)
    filtered_list.sort(key=lambda x:x[1])


    for model in filtered_list:
        window['-MLINE_KEY-'].write(model[0] + str(model[1]) + '\n')
        if stop_index:
            break
    window['-loading-'].update(visible=False)
    window['-stop2-'].update(visible=False)
    window.write_event_value('-sorting Done-', '')


def db_stats_window():



    layout = [[sg.Text('Model Count:')],
              [sg.Multiline(size=(80,20), write_only=True, auto_refresh=True, key='-stats-')], [sg.Button('Close', key='close')]]
    return sg.Window('DB Stats', layout, finalize=True, keep_on_top=True, grab_anywhere=True)


partsdict = read_db()
stop_index = False




layout = [  [sg.Text('Model prefix to search for:'), sg.Input(key='-prefix-', size=(6), enable_events=True),
             sg.Button('Filter', key='-filter-'),
             sg.pin(sg.Button('Stop', visible=False, key='-stop2-')), sg.Push(), sg.Button('Show All', key='-show all-'),
             sg.Button('Stop', visible=False, key='-stop-')],
            [sg.Text('Search Results:', font='Any 18'), sg.Text('LOADING...', font='Any 18', visible=False, key='-loading-'),
             sg.Text('INDEXING...', font='Any 18', visible=False, key='-indexing-')],
            [sg.Multiline(size=(80,20), key='-MLINE_KEY-', write_only=True, auto_refresh=True, autoscroll=True, disabled=True)],
            [sg.Button('Exit', key='-quit-', size=(7,1)), sg.pin(sg.ProgressBar(100, 'h', size=(30, 20), key='-progress-', visible=False)),
             sg.Push(), sg.Button('Re-Index Database', button_color='red', key='-index-')],
            [sg.Text('{} models in database'.format(len(partsdict['Models']))), sg.Button('DB Stats', key='-db_stats-'),
             sg.Push(), sg.Text('Last database index: {}'.format(partsdict['DB Date']), key='-db_date-')]]

window = sg.Window('Minco Active Model Finder', layout)


while True:
    event, values = window.read()
    # print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit', '-quit-', 'close'):
        break
    elif event == '-index-':
        stop_index = False
        index_button = sg.PopupYesNo('This will take a long time.', title='Are you sure?', font='Any 20')
        if index_button == 'Yes':
            window['-indexing-'].update(visible=True)
            window['-stop-'].update(visible=True)
            t1 = threading.Thread(target=reindex_thread, args=(window,), daemon=False)
            t1.start()

    elif event == '-show all-':
        stop_index = False
        window['-loading-'].update(visible=True)
        window['-stop-'].update(visible=True)
        window['-MLINE_KEY-'].update('')

        t2 = threading.Thread(target=show_all_thread, args=(window,), daemon=True)
        t2.start()

    elif event == '-filter-':
        prefix = values['-prefix-']
        window['-stop2-'].update(visible=True)
        stop_index = True
        window['-loading-'].update(visible=True)
        window['-MLINE_KEY-'].update('')
        stop_index = False
        t3 = threading.Thread(target=prefix_thread, args=(window,), daemon=False)
        t3.start()

    elif event == '-Indexing Done-':
        window['-indexing-'].update(visible=False)
        window['-stop-'].update(visible=False)

    elif event == '-db_stats-':
        stats = db_stats_window()
        prefix_list = []
        count = []
        for i in partsdict['Models']:
            prefix_list.append(i[0])
        pre_set = set(prefix_list)
        for pre in pre_set:
            count.append(pre + ': ' + str(prefix_list.count(pre)))

            stats['-stats-'].write(pre + ': ' + str(prefix_list.count(pre)) + '\n')
        while True:
            event, values = stats.read()
            if event in (sg.WIN_CLOSED, 'Exit', '-quit-', 'close'):
                stats.close()
                break


    elif event == '-stop-' or event == '-stop2-':
        stop_index = True



window.close()
stats.close()

