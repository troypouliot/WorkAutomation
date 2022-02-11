from os import walk, path, listdir
import pickle
import time
import pprint

F_DRIVE = 'F:\\Parts\\'.lower()
I_DRIVE = 'I:\\US\\Parts\\'.lower()
OLD_F_LOC = 'F:\\HEATERS\\Eng\\Parts\\'.lower()
OLD_I_LOC = 'I:\\US\\Heaters\\Eng\\Parts\\'.lower()
OLD_RUB_LOC = 'F:\\HEATERS\\Misc\\Plant2\\STANDARDS'.lower()
TREE_1 = ['3-Design'.lower(), '3_Design'.lower(), 'CAD'.lower()]
TREE_2 = ['304-CADCAM'.lower(), '304_CADCAM'.lower(), '303-CADCAM'.lower(), '303_CADCAM'.lower()]

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




def write_dict(prefix, model):
    global partsdict
    partsdict['DB Date'] = time.strftime('%Y-%m-%d %I:%M%p', time.localtime())
    try:
        partsdict['Models'].append((prefix, int(model)))
    except ValueError:
        pass
    return partsdict



def find_all_cur_f_loc_dict():
    for folderName, subfolders, filenames in walk(F_DRIVE):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in walk(path.join(F_DRIVE, sub)):
                for sub1 in subfolders1:
                    if not sub1.endswith('T'):
                        modelpath = path.join(F_DRIVE, sub, sub1)
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if path.exists(
                                                path.join(modelpath, tree1, tree2, sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                            print(sub1.strip('1234567890'), sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                                            write_dict(sub1.strip('1234567890'), sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                break
        break


def find_all_cur_i_loc_dict():
    for folderName, subfolders, filenames in walk(I_DRIVE):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in walk(path.join(I_DRIVE, sub)):
                for sub1 in subfolders1:
                    if not sub1.endswith('T'):
                        modelpath = path.join(I_DRIVE, sub, sub1)
                        for tree1 in TREE_1:
                            if path.exists(path.normcase(path.join(modelpath, tree1))):
                                for tree2 in TREE_2:
                                    if path.exists(path.join(modelpath, tree1, tree2)):
                                        if path.exists(
                                                path.join(modelpath, tree1, tree2, sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                            print(sub1.strip('1234567890'), sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                                            write_dict(sub1.strip('1234567890'), sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
                break
        break


def find_all_old_i_loc_dict():
    for folderName, subfolders, filenames in walk(OLD_I_LOC):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
                for sub1 in subfolders1:
                    modelpath = path.normcase(path.join(folderName, sub, sub1))
                    if check4CADFiles(modelpath) is True:
                        pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                        if pre != 'N' and len(pre) <= 5:
                            write_dict(pre, model)
                            print(pre, model)
                        continue
                    for tree1 in TREE_1:
                        if path.exists(path.normcase(path.join(modelpath, tree1))):
                            if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                pre, model = isActive(path.join(modelpath, tree1), '', sub1)
                                if pre != 'N' and len(pre) <= 5:
                                    write_dict(pre, model)
                                    print(pre, model)
                                continue
                            TREE_2.append(sub1)
                            for tree2 in TREE_2:
                                if path.exists(path.join(modelpath, tree1, tree2)):
                                    if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                                        pre, model = isActive(path.join(modelpath, tree1, tree2), '', sub1)
                                        if pre != 'N' and len(pre) <= 5:
                                            write_dict(pre, model)
                                            print(pre, model)
                            TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                break
        break

def find_all_old_f_loc_dict():
    for folderName, subfolders, filenames in walk(OLD_F_LOC):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
                for sub1 in subfolders1:
                    modelpath = path.normcase(path.join(folderName, sub, sub1))
                    if check4CADFiles(modelpath) is True:
                        pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                        if pre != 'N' and len(pre) <= 5:
                            write_dict(pre, model)
                            print(pre, model)
                        continue
                    for tree1 in TREE_1:
                        if path.exists(path.normcase(path.join(modelpath, tree1))):
                            if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                pre, model = isActive(path.join(modelpath, tree1), '', sub1)
                                if pre != 'N' and len(pre) <= 5:
                                    write_dict(pre, model)
                                    print(pre, model)
                                continue
                            TREE_2.append(sub1)
                            for tree2 in TREE_2:
                                if path.exists(path.join(modelpath, tree1, tree2)):
                                    if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                                        pre, model = isActive(path.join(modelpath, tree1, tree2), '', sub1)
                                        if pre != 'N' and len(pre) <= 5:
                                            write_dict(pre, model)
                                            print(pre, model)
                            TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                break
        break

def find_all_old_rub_loc_dict():
    for folderName, subfolders, filenames in walk(OLD_RUB_LOC):
        for sub in subfolders:
            # for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
            #     for sub1 in subfolders1:
                    modelpath = path.normcase(path.join(folderName, sub))
                    if check4CADFiles(modelpath) is True:
                        pre, model = isActive(path.join(folderName, sub), '', sub)
                        if pre != 'N' and len(pre) <= 5:
                            # write_dict(pre, model)
                            print(pre, model)
                        continue
                    for tree1 in TREE_1:
                        if path.exists(path.normcase(path.join(modelpath, tree1))):
                            if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                pre, model = isActive(path.join(folderName, sub, tree1), '', sub)
                                if pre != 'N' and len(pre) <= 5:
                                    # write_dict(pre, model)
                                    print(pre, model)
                                continue
                            # TREE_2.append(sub1)
                            # for tree2 in TREE_2:
                            #     if path.exists(path.join(modelpath, tree1, tree2)):
                            #         if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                            #             pre, model = isActive(path.join(folderName, sub, sub1), '', sub1)
                            #             if pre != 'N' and len(pre) <= 5:
                            #                 # write_dict(pre, model)
                            #                 print(pre, model)
                            # TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model

        break

def save_db(dict):
    with open('active_parts2', 'wb') as db:
        pickle.dump(dict, db)

def read_db():
    with open('active_parts', 'rb') as db:
        return pickle.load(db)

# partsdict = read_db()
partsdict = {'DB Date': '', 'Models': []}

find_all_old_f_loc_dict()
# find_all_old_i_loc_dict()
# find_all_cur_i_loc_dict()
# find_all_cur_f_loc_dict()
# find_all_old_rub_loc_dict()

# save_db(partsdict)



# pprint.pprint(partsdict)
print('{} models in DB'.format(len(partsdict['Models'])))

# for part in partsdict['Models']:
#     if part[0] == 'HSFAP':
#         print(part)