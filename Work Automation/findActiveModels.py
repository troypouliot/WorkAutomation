import os
import openpyxl
from time import time


def performance(fn):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = fn(*args, **kwargs)
        t2 = time()
        print('"{}" took {} s to run'.format(fn.__name__, t2 - t1))
        return result
    return wrapper


def countFiles(path):
    return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) - 1



def isActive(path, prefix, model_num):
    try:
        all_files = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
    except FileNotFoundError:
        return None
    key_files = []
    pre = []
    if countFiles(path) > 4:
        for file in all_files:
            if model_num.strip(prefix) in file:
                key_files.append(file.split(model_num)[0])
        for _ in key_files:
            if len(_) > 1:
                pre.append(_)
        if len(pre) > 0:
            # if max(set(pre), key=pre.count) == prefix:
            print(max(set(pre), key=pre.count), model_num)
            return max(set(pre), key=pre.count), model_num
            # else:
            #     return None
        else:
            return None
    else:
        return None


def check4CADFiles(path):
    cad_file_ext = ['.M', '.CAD', '.M1', '.M2', '.M3', '.STP']
    f_count = 0
    for ext in cad_file_ext:
        if cnt := len([name for name in os.listdir(path) if os.path.splitext(os.path.join(path, name))[1].upper() == ext]):
            f_count += cnt
    if f_count > 0:
        return True
    return False





partsList = []

f_drive = 'F:\\Parts\\'.lower()
i_drive = 'I:\\US\\Parts\\'.lower()
old_f_loc = 'F:\\HEATERS\\Eng\\Parts\\'.lower()
old_i_loc = 'I:\\US\\Heaters\\Eng\\Parts\\'.lower()
tree_1 = ['3-Design'.lower(), '3_Design'.lower(), 'CAD'.lower()]
tree_2 = ['304-CADCAM'.lower(), '304_CADCAM'.lower()]

###########################################################################
#   Use this to find specific model prefixes in the old F folder location
###########################################################################
@performance
def find_more_old_f_loc(pre):
    partPrefix = pre
    my_list = []
    for folderName, subfolders, filenames in os.walk(old_f_loc):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(old_f_loc, sub)):
                for sub1 in subfolders1:
                    my_list.append(isActive(os.path.join(old_f_loc, sub, sub1), partPrefix, sub1))
    print(my_list)



###########################################################################
#   Use this to find specific model prefixes in the current folder location
###########################################################################
@performance
def find_cur_f_loc(pre):
    # partPrefix = input('What model prefix are you looking for? ').upper()
    partPrefix = pre
    for folderName, subfolders, filenames in os.walk(f_drive):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(f_drive, sub)):
                for sub1 in subfolders1:
                    if sub1.endswith(partPrefix):
                        modelpath = os.path.join(f_drive, sub, sub1)
                        for tree1 in tree_1:
                            if os.path.exists(os.path.normcase(os.path.join(modelpath, tree1))):
                                for tree2 in tree_2:
                                    if os.path.exists(os.path.join(modelpath, tree1, tree2)):
                                        if os.path.exists(os.path.join(modelpath, tree1, tree2, sub1.strip(partPrefix))):
                                            print(partPrefix, sub1.split(partPrefix)[0])
                                            partsList.append(modelpath.upper())
                break
        break





@performance
def find_cur_i_loc(pre):
    partPrefix = pre
    for folderName, subfolders, filenames in os.walk(i_drive):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(i_drive, sub)):
                for sub1 in subfolders1:
                    if sub1.endswith(partPrefix):
                        modelpath = os.path.join(i_drive, sub, sub1)
                        for tree1 in tree_1:
                            if os.path.exists(os.path.normcase(os.path.join(modelpath, tree1))):
                                for tree2 in tree_2:
                                    if os.path.exists(os.path.join(modelpath, tree1, tree2)):
                                        if os.path.exists(os.path.join(modelpath, tree1, tree2, sub1.strip(partPrefix))):
                                            print(partPrefix, sub1.split(partPrefix)[0])
                                            partsList.append(modelpath.upper())
                break
        break


@performance
def find_old_i_loc():
    my_list = []
    for folderName, subfolders, filenames in os.walk(old_i_loc):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(folderName, sub)):
                for sub1 in subfolders1:
                    modelpath = os.path.normcase(os.path.join(folderName, sub, sub1))
                    if check4CADFiles(modelpath) is True:
                        my_list.append(isActive(os.path.join(folderName, sub, sub1), '', sub1))
                        continue
                    for tree1 in tree_1:
                        if os.path.exists(os.path.normcase(os.path.join(modelpath, tree1))):
                            if check4CADFiles(os.path.normcase(os.path.join(modelpath, tree1))):
                                my_list.append(isActive(os.path.join(folderName, sub, sub1, tree1), '', sub1))
                                continue
                            tree_2.append(sub1)
                            for tree2 in tree_2:
                                if os.path.exists(os.path.join(modelpath, tree1, tree2)):
                                    if check4CADFiles(os.path.normcase(os.path.join(modelpath, tree1, tree2))):
                                        my_list.append(isActive(os.path.join(folderName, sub, sub1, tree1, tree2), '', sub1))
                            tree_2.pop()    #  remove the sub1 item that was added to the tree_2 list since it is specific to the model
                break
        break

@performance
def find_more_old_i_loc(pre):
    partPrefix = pre
    my_list = []
    for folderName, subfolders, filenames in os.walk(old_i_loc):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(old_i_loc, sub)):
                for sub1 in subfolders1:
                    my_list.append(isActive(os.path.join(old_i_loc, sub, sub1), partPrefix, sub1))
    print(my_list)

for i in range(100):
    find_old_i_loc()


# find_cur_f_loc('HSAP')