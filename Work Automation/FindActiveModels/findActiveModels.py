from os import path, listdir, walk
import PySimpleGUI as sg
import pickle
import time
import threading


F_DRIVE = 'F:\\Parts\\'.lower()
I_DRIVE = 'I:\\US\\Parts\\'.lower()
OLD_F_LOC = 'F:\\HEATERS\\Eng\\Parts\\'.lower()
OLD_I_LOC = 'I:\\US\\Heaters\\Eng\\Parts\\'.lower()
OLD_RUB_LOC = 'F:\\HEATERS\\Misc\\Plant2\\STANDARDS'.lower()
TREE_1 = ['3-Design'.lower(), '3_Design'.lower(), 'CAD'.lower()]
TREE_2 = ['304-CADCAM'.lower(), '304_CADCAM'.lower()]


def count_files(dir_path):
    return len([name for name in listdir(dir_path) if path.isfile(path.join(dir_path, name))]) - 1


def is_active(dir_path, model_num):
    try:
        all_files = [name for name in listdir(dir_path) if path.isfile(path.join(dir_path, name))]
    except FileNotFoundError:
        return 'NA'
    key_files = []
    pre = []
    if count_files(dir_path) > 4:
        for file in all_files:
            if model_num in file:
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


def check_4_cad_files(dir_path):
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


def write_to_dict(pre, model):
    global partsdict
    partsdict['DB Date'] = time.strftime('%Y-%m-%d %I:%M%p', time.localtime())
    try:
        partsdict['Models'].append((pre, int(model)))
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
                        if not sub1.endswith('T'):
                            modelpath = path.join(F_DRIVE, sub, sub1)
                            for tree1 in TREE_1:
                                if path.exists(path.normcase(path.join(modelpath, tree1))):
                                    for tree2 in TREE_2:
                                        if path.exists(path.join(modelpath, tree1, tree2)):
                                            if path.exists(path.join(modelpath, tree1, tree2,
                                                                     sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                                write_to_dict(sub1.strip('1234567890'),
                                                              sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                                                window['-MLINE_KEY-'].write(sub1.strip('1234567890') +
                                                                            sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ') +
                                                                            '\n')
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
                        if check_4_cad_files(modelpath) is True:
                            pre, model = is_active(path.join(folderName, sub, sub1), sub1)
                            if pre != 'N' and len(pre) <= 5:
                                write_to_dict(pre, model)
                                window['-MLINE_KEY-'].write(pre + model + '\n')
                                if stop_index:
                                    raise StopIteration
                            continue
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                if check_4_cad_files(path.normcase(path.join(modelpath, tree1))):
                                    pre, model = is_active(path.join(modelpath, tree1), sub1)
                                    if pre != 'N' and len(pre) <= 5:
                                        write_to_dict(pre, model)
                                        window['-MLINE_KEY-'].write(pre + model + '\n')
                                        if stop_index:
                                            raise StopIteration
                                    continue
                                TREE_2.append(sub1)
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if check_4_cad_files(path.normcase(path.join(modelpath, tree1, tree2))):
                                            pre, model = is_active(path.join(modelpath, tree1, tree2), sub1)
                                            if pre != 'N' and len(pre) <= 5:
                                                write_to_dict(pre, model)
                                                window['-MLINE_KEY-'].write(pre + model + '\n')
                                                if stop_index:
                                                    raise StopIteration
                                TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is
                                # specific to the model
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
                        if not sub1.endswith('T'):
                            modelpath = path.join(I_DRIVE, sub, sub1)
                            for tree1 in TREE_1:
                                if path.exists(path.normcase(path.join(modelpath, tree1))):
                                    for tree2 in TREE_2:
                                        if path.exists(path.join(modelpath, tree1, tree2)):
                                            if path.exists(
                                                    path.join(modelpath, tree1, tree2,
                                                              sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                                write_to_dict(sub1.strip('1234567890'),
                                                              sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                                                window['-MLINE_KEY-'].write(sub1.strip('1234567890') +
                                                                            sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ') +
                                                                            '\n')
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
                        if check_4_cad_files(modelpath) is True:
                            pre, model = is_active(path.join(folderName, sub, sub1), sub1)
                            if pre != 'N' and len(pre) <= 5:
                                write_to_dict(pre, model)
                                window['-MLINE_KEY-'].write(pre + model + '\n')
                            if stop_index:
                                raise StopIteration
                            continue
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                if check_4_cad_files(path.normcase(path.join(modelpath, tree1))):
                                    pre, model = is_active(path.join(modelpath, tree1), sub1)
                                    if pre != 'N' and len(pre) <= 5:
                                        write_to_dict(pre, model)
                                        window['-MLINE_KEY-'].write(pre + model + '\n')
                                    if stop_index:
                                        raise StopIteration
                                    continue
                                TREE_2.append(sub1)
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if check_4_cad_files(path.normcase(path.join(modelpath, tree1, tree2))):
                                            pre, model = is_active(path.join(modelpath, tree1, tree2), sub1)
                                            if pre != 'N' and len(pre) <= 5:
                                                write_to_dict(pre, model)
                                                window['-MLINE_KEY-'].write(pre + model + '\n')
                                            if stop_index:
                                                raise StopIteration
                                TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is
                                # specific to the model
                    break
            break
    except StopIteration:
        pass


def find_old_rub_loc():
    try:
        for folderName, subfolders, filenames in walk(OLD_RUB_LOC):
            for sub in subfolders:
                if stop_index:
                    raise StopIteration
                modelpath = path.normcase(path.join(folderName, sub))
                if check_4_cad_files(modelpath) is True:
                    pre, model = is_active(path.join(folderName, sub), sub)
                    if pre != 'N' and len(pre) <= 5:
                        write_to_dict(pre, model)
                        window['-MLINE_KEY-'].write(pre + model + '\n')
                    if stop_index:
                        raise StopIteration
                    continue
                for tree1 in TREE_1:
                    if path.exists(path.normcase(path.join(modelpath, tree1))):
                        if check_4_cad_files(path.normcase(path.join(modelpath, tree1))):
                            pre, model = is_active(path.join(folderName, sub, tree1), sub)
                            if pre != 'N' and len(pre) <= 5:
                                write_to_dict(pre, model)
                                window['-MLINE_KEY-'].write(pre + model + '\n')
                            if stop_index:
                                raise StopIteration
                            continue
            break
    except StopIteration:
        pass


def reindex_dict(wind):
    global partsdict
    partsdict['DB Date'] = 'NA'
    partsdict['Models'] = []
    wind['-progress-'].update(0, 100, visible=True)
    find_cur_f_loc()
    wind['-progress-'].update(20, 100)
    find_cur_i_loc()
    wind['-progress-'].update(40, 100)
    find_old_i_loc()
    wind['-progress-'].update(60, 100)
    find_old_f_loc()
    wind['-progress-'].update(80, 100)
    find_old_rub_loc()
    wind['-progress-'].update(99, 100)
    save_db(partsdict)
    wind['-progress-'].update(100, 100, visible=False)
    wind['-db_date-'].update('Last database index: {}'.format(read_db()['DB Date']))
    wind['-count'].update('{} models in database'.format(len(partsdict['Models'])))
    wind.write_event_value('-Indexing Done-', '')


def show_all_models(wind):
    filtered_list = []
    for model in partsdict['Models']:
        filtered_list.append(model)
        if stop_index:
            break
    filtered_list.sort(key=lambda x: x[1])

    for model in filtered_list:
        wind['-MLINE_KEY-'].write(model[0] + str(model[1]) + '\n')
        if stop_index:
            break
    wind['-loading-'].update(visible=False)
    wind.write_event_value('-Indexing Done-', '')


def filter_list(wind):
    wind['-MLINE_KEY-'].update('')
    filtered_list = []
    for model in partsdict['Models']:
        if model[0] == wind['-prefix-'].get().upper():
            filtered_list.append(model)
    filtered_list.sort(key=lambda x: x[1])
    for model in filtered_list:
        wind['-MLINE_KEY-'].write(model[0] + str(model[1]) + '\n')
        if stop_index:
            break
    wind['-loading-'].update(visible=False)
    wind['-stop2-'].update(visible=False)
    wind.write_event_value('-sorting Done-', '')


def db_stats_window():
    prefix_list = []
    count = []
    for i in partsdict['Models']:
        prefix_list.append(i[0])
    pre_set = set(prefix_list)

    for pre in pre_set:
        count.append((pre, prefix_list.count(pre)))

    count.sort(key=lambda x:x[1], reverse=True)
    excluded = ['$', '~', '_', '-']
    new_list = []
    for i in count:
        if len(i[0]) > 0 and i[1] > 1:
            if not any(x in i[0] for x in excluded):
                new_list.append(str(i))
    return sg.popup_scrolled(*new_list, size=(30,30), title='Database Stats', grab_anywhere=True,
                             icon=b'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')


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
            [sg.Text('{} models in database'.format(len(partsdict['Models'])), key='-count-'), sg.Button('DB Stats', key='-db_stats-'),
             sg.Push(), sg.Text('Last database index: {}'.format(partsdict['DB Date']), key='-db_date-')]]

window = sg.Window('Minco Active Model Finder', layout,
                   icon=b'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')

while True:
    event, values = window.read()
    print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit', '-quit-', 'close'):
        break
    elif event == '-index-':
        stop_index = False
        index_button = sg.PopupYesNo('This will take a long time.', title='Are you sure?', font='Any 20')
        if index_button == 'Yes':
            window['-indexing-'].update(visible=True)
            window['-stop-'].update(visible=True)
            t1 = threading.Thread(target=reindex_dict, args=(window,), daemon=False)
            t1.start()

    elif event == '-show all-':
        stop_index = False
        window['-loading-'].update(visible=True)
        window['-stop-'].update(visible=True)
        window['-MLINE_KEY-'].update('')

        t2 = threading.Thread(target=show_all_models, args=(window,), daemon=True)
        t2.start()

    elif event == '-filter-':
        prefix = values['-prefix-']
        window['-stop2-'].update(visible=True)
        window['-loading-'].update(visible=True)
        window['-MLINE_KEY-'].update('')
        stop_index = False
        t3 = threading.Thread(target=filter_list, args=(window,), daemon=False)
        t3.start()

    elif event == '-Indexing Done-':
        window['-indexing-'].update(visible=False)
        window['-stop-'].update(visible=False)

    elif event == '-db_stats-':
        stats = db_stats_window()

    elif event == '-stop-' or '-stop2-':
        stop_index = True
        window['-stop-'].update(visible=False)

window.close()
