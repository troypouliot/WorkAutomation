from os import walk, path, listdir
import pickle
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

def write_list(inp):
    old_list = []
    with open('parts_list.txt', 'r') as db:
        for line in db.readlines():
            old_list.append(line.strip('\n'))
    new_list = set(inp)
    combined = new_list.union(old_list)
    with open('parts_list.txt', 'w') as db:
        for part in combined:
            db.write(part + '\n')



def find_all_cur_f_loc():
    partslist = []
    partcount = 0
    for folderName, subfolders, filenames in walk(F_DRIVE):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in walk(path.join(F_DRIVE, sub)):
                for sub1 in subfolders1:

                    # if sub1.endswith(partPrefix):
                    modelpath = path.join(F_DRIVE, sub, sub1)
                    for tree1 in TREE_1:

                        if path.exists(path.normcase(path.join(modelpath, tree1))):
                            for tree2 in TREE_2:

                                if path.exists(path.join(modelpath, tree1, tree2)):
                                    if path.exists(
                                            path.join(modelpath, tree1, tree2, sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                        partcount += 1
                                        partslist.append(sub1)
                                        print(sub1)
                                        write_list(partslist)
                break
        break

    print('Done. Found {} active model'.format(partcount))

def find_all_cur_i_loc():

    partslist = []
    partcount = 0
    for folderName, subfolders, filenames in walk(I_DRIVE):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in walk(path.join(I_DRIVE, sub)):
                for sub1 in subfolders1:

                    modelpath = path.join(I_DRIVE, sub, sub1)
                    for tree1 in TREE_1:
                        if path.exists(path.normcase(path.join(modelpath, tree1))):
                            for tree2 in TREE_2:
                                if path.exists(path.join(modelpath, tree1, tree2)):
                                    if path.exists(
                                            path.join(modelpath, tree1, tree2, sub1.strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))):
                                        # print(partPrefix, sub1.split(partPrefix)[0])
                                        partcount += 1
                                        partslist.append(sub1)
                                        print(sub1)
                                        write_list(partslist)
                break
        break
    print('Done. Found {} active model'.format(partcount))

def find_all_old_i_loc():
    partslist = []
    partcount = 0
    model_list = []
    for folderName, subfolders, filenames in walk(OLD_I_LOC):
        for sub in subfolders:
            for folderName1, subfolders1, filenames1 in walk(path.join(folderName, sub)):
                for sub1 in subfolders1:
                    modelpath = path.normcase(path.join(folderName, sub, sub1))
                    if check4CADFiles(modelpath) is True:
                        model_list.append(isActive(path.join(folderName, sub, sub1), '', sub1))
                        print(model_list[-1])
                        continue
                    for tree1 in TREE_1:
                        if path.exists(path.normcase(path.join(modelpath, tree1))):
                            if check4CADFiles(path.normcase(path.join(modelpath, tree1))):
                                model_list.append(isActive(path.join(folderName, sub, sub1, tree1), '', sub1))
                                print(model_list[-1])
                                continue
                            TREE_2.append(sub1)
                            for tree2 in TREE_2:
                                if path.exists(path.join(modelpath, tree1, tree2)):
                                    if check4CADFiles(path.normcase(path.join(modelpath, tree1, tree2))):
                                        model_list.append(
                                            isActive(path.join(folderName, sub, sub1, tree1, tree2), '', sub1))
                                        print(model_list[-1])

                            TREE_2.pop()  # remove the sub1 item that was added to the tree_2 list since it is specific to the model
                break
        break


find_all_old_i_loc()