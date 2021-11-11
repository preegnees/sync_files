import sys
import os


list_of_all_paths = []
list_of_all_paths_for_compare = []

def check_platform(path):
    lin_delimetr = "/"
    win_delimetr = "\\"
    delimetr = None
    if win_delimetr in path:
        delimetr = win_delimetr
    elif lin_delimetr in path:
        delimetr = lin_delimetr
    else:
        print("платфорама не распознана")
        sys.exit() 
    start_folder = path.split(delimetr)[-1]
    split_dir = path.split(delimetr)
    position = split_dir.index(start_folder)
    return (delimetr, position)
def rename_on_fix_name(fix_file, path, delimetr):
    src = path
    tmp_file = path.split(delimetr)[0:-1]
    dst = delimetr.join(tmp_file) + delimetr + fix_file
    os.rename(src, dst)
def fix_spaces(path, delimetr):
    file = path.split(delimetr)[-1]
    tmp_file = file.split(" ")
    fix_file = "_".join(tmp_file)
    tmp_file = fix_file.split("\xa0")
    fix_file = "_".join(tmp_file)
    rename_on_fix_name(fix_file, path, delimetr)
def check_spaces(name, path, delimetr):
    temp_list = name.split(" ")
    if len(temp_list) >= 2:
        fix_spaces(path, delimetr)
    
def check_schema(path, delimetr, position):
    list_of_dir = os.listdir(path)
    for i in list_of_dir:
        current_path = path + delimetr + i 
        check_spaces(i, current_path, delimetr)
        if os.path.isdir(current_path):
            check_spaces(i, current_path, delimetr)
            check_schema(current_path, delimetr, position)
            tmp_curr_path = delimetr + delimetr.join(current_path.split(delimetr)[position+1:len(current_path)])
            list_of_all_paths.append(tmp_curr_path)

def compare(list_1, list_2):
    unique_in_list_1 = []
    unique_in_list_2 = []
    
    for i in list_1:
        key_a = 0
        for j in list_2:
            if i == j:
                key_a += 1
        if key_a == 0:
            unique_in_list_1.append(i) 
    for i in list_2:
        key_a = 0
        for j in list_1:
            if i == j:
                key_a += 1
        if key_a == 0:
            unique_in_list_2.append(i) 
    return (unique_in_list_1, unique_in_list_2)

def create_folders(path_1, path_2):
    pass

def input_controll():
    print("Для синхронизации введите пути через пробел, исспользовать файл cache_dir.txt [1]")
    path_1 = None
    path_2 = None
    
    inp = input()
    try:
        inp = int(inp)
        with open("cache_dir.txt", "r+") as file:
            cahe = file.read()  
        path_1 = cahe.split(" ")[0]
        path_2 = cahe.split(" ")[1]
    except:
        print("cache_dir.txt скорее всего пустой, введите пути через пробел")
        inp = input()
        path_1 = inp.split(" ")[0]
        path_2 = inp.split(" ")[1]
    return (path_1, path_2)
def input_create_folder(unique_in_list_1, unique_in_list_2, path_1, path_2, delimiter):
        inp = ""
        while inp != "q":
            print("введите способ [1]: 1--->2, [2]: 2--->1, [3]: 1<--->2), назад [q]")

            inp = input()
            if inp == "q":
                return
            else:
                try:
                    inp = int(inp)
                except:
                    return
            if inp == 1:
                for i in unique_in_list_1:
                    dir_name = path_2 + i
                    try:
                        os.makedirs(dir_name)
                    except:
                        pass
            if inp == 2:
                for i in unique_in_list_2:
                    dir_name = path_1 + i
                    try:
                        os.makedirs(dir_name)
                    except:
                        pass
            if inp == 3:
                for i in unique_in_list_2:
                    dir_name = path_1 + i
                    try:
                        os.makedirs(dir_name)
                    except:
                        pass
                for i in unique_in_list_1:
                    dir_name = path_2 + i
                    try:
                        os.makedirs(dir_name)
                    except:
                        pass
def delete_space():
    print("Для успешной синхронизации дирикторий нужно, что бы названиях файлов или папок не было пробелов, желаете их заменить на _ , да [1], нет [0], назад [q]\n" + \
        "важно, что бы в изначальном пути, который вы сейчас укажите, не было названий с пробелами")
    inp = input()
    try:
        inp = int(inp)
        if inp == 1:
            inp = 1
        if inp == 0:
            return
    except:
        if inp == "q":
            return
        else:
            return
    if inp == 1:
        print("Введите директории, с которыми вы хотите сделать операцию, исспользовать файл cache_dir.txt [1], назад [q] ")
        dir = input()
        try:
            inp = int(inp)
            with open("cache_dir.txt", "r+") as file:
                cahe = file.read()  
            path_1 = cahe.split(" ")[0]
            path_2 = cahe.split(" ")[1]
        except:
            print("cache_dir.txt скорее всего пустой, введите пути через пробел")
            inp = input()
            path_1 = inp.split(" ")[0]
            path_2 = inp.split(" ")[1]
        
        if dir == "q":
            return
        path_1 = dir.split(" ")[0]
        path_2 = dir.split(" ")[1]
        
        (delimetr, position) = check_platform(path_1)
        check_schema(path_1, delimetr, position)
        (delimetr, position) = check_platform(path_2)
        check_schema(path_2, delimetr, position)
        with open("cache_dir.txt", "w+") as file:
            file.write(path_1 + " " + path_2)
        print("Успешно заменено, записано в cache_dir.txt")


def main_folder():
    delete_space()
    list_of_all_paths.clear()

    (path_1, path_2) = input_controll()
    (delimetr, position) = check_platform(path_1)
    check_schema(path_1, delimetr, position)
    
    list_of_all_paths_for_compare = list(list_of_all_paths)
    list_of_all_paths.clear()

    (delimetr, position) = check_platform(path_2)    
    check_schema(path_2, delimetr, position)

    (unique_in_list_1, unique_in_list_2) = compare(list_of_all_paths_for_compare, list_of_all_paths)
    print("Есть только в ", path_1)
    print(unique_in_list_1)
    print("")
    print("Есть только в ", path_2)
    print(unique_in_list_2)
    print("")

    input_create_folder(unique_in_list_1, unique_in_list_2, path_1, path_2, delimetr)
