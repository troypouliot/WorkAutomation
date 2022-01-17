import os

F_DRIVE = 'F:\\Parts\\'.lower()
I_DRIVE = 'I:\\US\\Parts\\'.lower()
OLD_F_LOC = 'F:\\HEATERS\\Eng\\Parts\\'.lower()
OLD_I_LOC = 'I:\\US\\Heaters\\Eng\\Parts\\'.lower()
TREE_1 = ['3-Design'.lower(), '3_Design'.lower(), 'CAD'.lower()]
TREE_2 = ['304-CADCAM'.lower(), '304_CADCAM'.lower()]


def countFiles(path):
    return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) - 1


def isActive(path, prefix, model_num):
    try:
        all_files = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
    except FileNotFoundError:
        return 'NA'
    key_files = []
    pre = []
    if countFiles(path) > 4:
        for file in all_files:
            if model_num.strip(prefix) in file:
                key_files.append(file.split(model_num)[0])
        for _ in key_files:
            if len(_) > 1:
                pre.append(_.upper())
        if len(pre) > 0:
            # if max(set(pre), key=pre.count) == prefix:
            # print(max(set(pre), key=pre.count), model_num)
            return max(set(pre), key=pre.count), model_num
            # else:
            #     return None
        else:
            return 'NA'
    else:
        return 'NA'


def check4CADFiles(path):
    cad_file_ext = ['.M', '.CAD', '.M1', '.M2', '.M3', '.STP']
    f_count = 0
    for ext in cad_file_ext:
        if cnt := len(
                [name for name in os.listdir(path) if os.path.splitext(os.path.join(path, name))[1].upper() == ext]):
            f_count += cnt
    if f_count > 0:
        return True
    return False


###########################################################################
#   Use this to find specific model prefixes in the current F folder location
###########################################################################
def find_cur_f_loc(pre):
    # partPrefix = input('What model prefix are you looking for? ').upper()
    partPrefix = pre
    for folderName, subfolders, filenames in os.walk(F_DRIVE):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(F_DRIVE, sub)):
                for sub1 in subfolders1:
                    if sub1.endswith(partPrefix):
                        modelpath = os.path.join(F_DRIVE, sub, sub1)
                        for tree1 in TREE_1:
                            if os.path.exists(os.path.normcase(os.path.join(modelpath, tree1))):
                                for tree2 in TREE_2:
                                    if os.path.exists(os.path.join(modelpath, tree1, tree2)):
                                        if os.path.exists(
                                                os.path.join(modelpath, tree1, tree2, sub1.strip(partPrefix))):
                                            print(partPrefix, sub1.split(partPrefix)[0])
                                            # partsList.append(modelpath.upper())
                break
        break


###########################################################################
#   Use this to find specific model prefixes in the old F folder location
###########################################################################
def find_old_f_loc(pre=''):
    pre = pre.upper()
    my_list = []
    for folderName, subfolders, filenames in os.walk(OLD_F_LOC):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(folderName, sub)):
                for sub1 in subfolders1:
                    modelpath = os.path.normcase(os.path.join(folderName, sub, sub1))
                    if check4CADFiles(modelpath) is True:
                        my_list.append(isActive(os.path.join(folderName, sub, sub1), '', sub1))
                        if pre == '':
                            continue
                        if my_list[-1][0] != pre:
                            my_list.pop()
                        else:
                            print(my_list[-1])
                        continue
                    for tree1 in TREE_1:
                        if os.path.exists(os.path.normcase(os.path.join(modelpath, tree1))):
                            if check4CADFiles(os.path.normcase(os.path.join(modelpath, tree1))):
                                my_list.append(isActive(os.path.join(folderName, sub, sub1, tree1), '', sub1))
                                if pre == '':
                                    continue
                                if my_list[-1][0] != pre:
                                    my_list.pop()
                                else:
                                    print(my_list[-1])
                                continue
                            TREE_2.append(sub1)
                            for tree2 in TREE_2:
                                if os.path.exists(os.path.join(modelpath, tree1, tree2)):
                                    if check4CADFiles(os.path.normcase(os.path.join(modelpath, tree1, tree2))):
                                        my_list.append(
                                            isActive(os.path.join(folderName, sub, sub1, tree1, tree2), '', sub1))
                                        if pre == '':
                                            continue
                                        if my_list[-1][0] != pre:
                                            my_list.pop()
                                        else:
                                            print(my_list[-1])
                            TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                break
        break
    return '{} models found'.format(len(my_list)), my_list


#################################################################################
#   Use this to find specific model prefixes in the current I folder location   #
#################################################################################
def find_cur_i_loc(pre):
    partPrefix = pre
    for folderName, subfolders, filenames in os.walk(I_DRIVE):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(I_DRIVE, sub)):
                for sub1 in subfolders1:
                    if sub1.endswith(partPrefix):
                        modelpath = os.path.join(I_DRIVE, sub, sub1)
                        for tree1 in TREE_1:
                            if os.path.exists(os.path.normcase(os.path.join(modelpath, tree1))):
                                for tree2 in TREE_2:
                                    if os.path.exists(os.path.join(modelpath, tree1, tree2)):
                                        if os.path.exists(
                                                os.path.join(modelpath, tree1, tree2, sub1.strip(partPrefix))):
                                            print(partPrefix, sub1.split(partPrefix)[0])
                                            # partsList.append(modelpath.upper())
                break
        break


#################################################################################
#   Use this to find specific model prefixes in the old I folder location       #
#################################################################################
def find_old_i_loc(pre=''):
    pre = pre.upper()
    my_list = []
    for folderName, subfolders, filenames in os.walk(OLD_I_LOC):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in os.walk(os.path.join(folderName, sub)):
                for sub1 in subfolders1:
                    modelpath = os.path.normcase(os.path.join(folderName, sub, sub1))
                    if check4CADFiles(modelpath) is True:
                        my_list.append(isActive(os.path.join(folderName, sub, sub1), '', sub1))
                        if pre == '':
                            continue
                        if my_list[-1][0] != pre:
                            my_list.pop()
                        continue
                    for tree1 in TREE_1:
                        if os.path.exists(os.path.normcase(os.path.join(modelpath, tree1))):
                            if check4CADFiles(os.path.normcase(os.path.join(modelpath, tree1))):
                                my_list.append(isActive(os.path.join(folderName, sub, sub1, tree1), '', sub1))
                                if pre == '':
                                    continue
                                if my_list[-1][0] != pre:
                                    my_list.pop()
                                continue
                            TREE_2.append(sub1)
                            for tree2 in TREE_2:
                                if os.path.exists(os.path.join(modelpath, tree1, tree2)):
                                    if check4CADFiles(os.path.normcase(os.path.join(modelpath, tree1, tree2))):
                                        my_list.append(
                                            isActive(os.path.join(folderName, sub, sub1, tree1, tree2), '', sub1))
                                        if pre == '':
                                            continue
                                        if my_list[-1][0] != pre:
                                            my_list.pop()
                            TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                break
        break
    return '{} models found'.format(len(my_list)), my_list


# print(find_old_i_loc('hr'))


# find_cur_i_loc('HSAP')
find_cur_f_loc('HSK')
# find_old_f_loc('HSFAP')
