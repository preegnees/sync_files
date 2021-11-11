import os
import datetime as dt
from modif import *
from check_dir import main_folder
from check_dir import check_platform


dict_of_file_time = {}



text_path = "путь: "
text_file = "файлы: "
text_all_count_files = "файлов всего: "
text_file_only_in_one = "файлы, которые есть только в первой группе: "
text_file_only_in_two = "файлы, которые есть только во второй группе: "
text_file_newer_in_one = "файлы, которые новее в первой группе: "
text_file_newer_in_two = "файлы, которые новее во второй группе: "
text_file_which_in_one_and_in_two = "файл, которых однакове время изменения: "

menu_sync = "[1]    замена оригинальных файлов на более новые;\n" + \
            "[2]    добавление уникальных файлов;\n" + \
            "[3]    копирование дополнительных префиксных файлов ;\n" + \
            "[4]    копирование с заменой всех предыдущих префиксных файлов на один новый префиксный;\n" + \
            "[q]    назад;\n" + \
            "вид:   1/2/3/4-(напрвление директорий (a,b): 1 (a<-->b), 2 (a->b), 3 (b->a));\n" + \
            "[ можжно делать несколько вводов через пробелы]\n" + \
            "[если вы что то изменили в файлах пока находились в этом меню, вам нужно вернуться назад q и проанализировать файлы заново];"
file_cache = "cache_dir.txt"
start_or_quit = "[1]    начать;\n" + \
                "[q]    выйти из программы;"
watch_all_or_analys_or_quit = "[1]    показать все файлы;\n" + \
                              "[2]    анализировать;\n" + \
                              "[q]    выйти из программы;"
write_paths = "[->]   введите 2 директории через пробел (без экранирования, не добавляя вконце пути \\ (/), все названия должны быть без пробелов);\n" + \
              "[d]    синхронизировать струтуру дирикторий, обязательно, если вы не увернеы, что она одинаковая;\n" + \
              "[t]    тест;\n" + \
              "[e]    последнее значение из кэш-файла;\n" + \
              "[q]    выйти из программы;"
does_not_cache_file = "файла нет"
strange_cache_file = "странный кэш"
uncorrent_write = "ваш ввод некорректен"
no_recognized = "не распознано"

action_examination = "1234"
vector_examination = "123"

quit = "q"
test = "t"
dir = "d"
end_record_cache = "e"
start_number = "1"
watch_all_files = "1"
analys_number = "2"
action_one = "1"
action_two = "2"
action_three = "3"
action_four = "4"
vector_all_one_two = "1"
vector_one_in_two = "2"
vector_two_in_one = "3"

def input_paths():
    lst_paths = []
    inp = ""
    while(inp != quit):

        print(write_paths)
        inp = input()
        if inp == dir:
            main_folder()
        elif inp == quit:
            raise SystemExit(1)
        elif inp == end_record_cache:
            lst_paths_str = ""
            temp_lst_paths = []
            try:
                file = open(file_cache)
            except IOError as e:
                print(does_not_cache_file)
            try:
                with open(file_cache, "r+") as file:
                    lst_paths_str = file.read()
                for l in lst_paths_str:
                    temp_lst_paths.append(l)
                temp_lst_paths = "".join(temp_lst_paths).split(" ")
                for l in temp_lst_paths:
                    lst_paths.append(l)
            except:
                print(strange_cache_file)
                continue
            
            print(lst_paths)

            
        elif len(inp.split(" ")) > 2 or len(inp.split(" ")) <= 1:
            print(uncorrent_write)
            continue
        
        else:
            inps = inp.split(" ")
            for p in inps:
                lst_paths.append(p)

            with open(file_cache, "w+") as file:
                file.write(inp)
        delimiter_main = check_platform(lst_paths[0])            
        return lst_paths, delimiter_main

def __get_time(file_path):
    no_formating_date_no_spliting = str(dt.datetime.fromtimestamp(os.path.getmtime(file_path))).split('.')[0]
    no_formating_date = str(no_formating_date_no_spliting).split(" ")
    ymd_no_form = no_formating_date[0].split("-")
    ymd = "".join(ymd_no_form)
    
    hms_no_form = no_formating_date[1].split(":")
    s = hms_no_form[2].split(".")[0]
    hms_no_form[2] = s
    hms = "".join(hms_no_form)
    
    date = int(ymd + hms)
    return (date, no_formating_date_no_spliting)
    
def __get_all_file(full_path_file):
    (t, full_time) = __get_time(full_path_file)
    dict_of_file_time[full_path_file] = (t, full_time)

def __recurse_search_dir(owner_path, delimiter_main):
    temp_dict = {}
    delimiter_main = delimiter_main[0]
    list_dir = os.listdir(owner_path)
    for file_in_dir in list_dir:
        full_path_file = owner_path + delimiter_main + file_in_dir
        if os.path.isdir(full_path_file):
            __recurse_search_dir(full_path_file, delimiter_main)
            
        else:
            __get_all_file(full_path_file)

            
    temp_dict = dict_of_file_time.copy()
    return temp_dict

def get_full_files_of_all_pasths(lst_paths, delimetr_main):
    delimetr_main = delimetr_main[0]
    lst_full_files_all_paths = {}
    for p in lst_paths:
        temp_dict = __recurse_search_dir(p, delimetr_main)
        dict_of_file_time.clear()
        lst_full_files_all_paths[p] = temp_dict
    return lst_full_files_all_paths

def print_files(lst_full_files_all_paths):
    
    files = 0
    for i in lst_full_files_all_paths:
        print(text_path, i)
        print(text_file)
        for f in lst_full_files_all_paths.get(i):
            files += 1
            print(f, ", ", lst_full_files_all_paths.get(i).get(f))
        print("")
    print(text_all_count_files, files)



def syncronize(full_paths, lst_path, delimetr_main):
    delimetr_main = delimetr_main[0] 
    temp_one = []
    temp_two = []

    file_only_in_one = []
    file_only_in_two = []
    file_which_in_one_and_in_two = []
    file_newer_in_one = []
    file_newer_in_two = []
    temp_one_temp_two = []
    all_other = []

    keyses = full_paths.keys()
    all_keys = []
    for i in keyses:
        all_keys.append(i)
    temp_one.append(full_paths.get(all_keys[0]))
    temp_two.append(full_paths.get(all_keys[1]))

    delimetr_one = len(lst_path[0].split(delimetr_main)) - 1
    delimetr_two = len(lst_path[1].split(delimetr_main)) - 1

    for i in temp_one[0]:
        temp_i = i.split(delimetr_main)[delimetr_one+1:len(i)]
        join_temp_i = delimetr_main + delimetr_main.join(temp_i)
        tr_equals_i = 0
        tr_more_i = 0
        tr_less_i = 0

        for j in temp_two[0]:
            temp_j = j.split(delimetr_main)[delimetr_two+1:len(j)]
            join_temp_j = delimetr_main + delimetr_main.join(temp_j)
            
            if join_temp_i == join_temp_j:
                tr_equals_i = 0
                tr_more_i = 0
                tr_less_i = 0

                if int(temp_one[0].get(i)[0]) == int(temp_two[0].get(j)[0]):
                    file_which_in_one_and_in_two.append(join_temp_i)
                    tr_equals_i = 1
                elif int(temp_one[0].get(i)[0]) > int(temp_two[0].get(j)[0]):
                    file_newer_in_one.append(join_temp_i)
                    tr_more_i = 1
                elif int(temp_one[0].get(i)[0]) < int(temp_two[0].get(j)[0]):
                    file_newer_in_two.append(join_temp_j)
                    tr_less_i = 1
                
        if tr_equals_i == 0 and tr_more_i == 0 and tr_less_i == 0:
            file_only_in_one.append(join_temp_i)
    
    for i in temp_one[0]:
        a  = i.split(delimetr_main)[delimetr_one+1:len(i)]
        b = delimetr_main + delimetr_main.join(a)
        temp_one_temp_two.append(b)
    for i in temp_two[0]:
        a  = i.split(delimetr_main)[delimetr_two+1:len(i)]
        b = delimetr_main + delimetr_main.join(a)
        temp_one_temp_two.append(b)
    for i in file_only_in_one:
        all_other.append(i)
    for i in file_which_in_one_and_in_two:
        all_other.append(i)
    for i in file_newer_in_one:
        all_other.append(i)
    for i in file_newer_in_two:
        all_other.append(i)

    temp_temp_one_temp_two = list(temp_one_temp_two)
    for i in all_other:
        for j in temp_temp_one_temp_two:
            k = len(temp_temp_one_temp_two)
            while k > 0:
                k -= 1
                if i == j:
                    try:
                        temp_temp_one_temp_two.remove(i)
                    except:
                        continue                
    file_only_in_two = list(temp_temp_one_temp_two)

    print(text_file_only_in_one, file_only_in_one)
    print(text_file_only_in_two, file_only_in_two)
    print(text_file_newer_in_one, file_newer_in_one)
    print(text_file_newer_in_two, file_newer_in_two)
    print(text_file_which_in_one_and_in_two, file_which_in_one_and_in_two)
    return (file_only_in_one, file_only_in_two, file_newer_in_one, file_newer_in_two, file_which_in_one_and_in_two, lst_path)

        


def print_sync_info():
    print(menu_sync)

def syn_all_newer_on_noprefix_file(file_newer_in_one, file_newer_in_two, lst_path, vector, delimetr_main):
    path_1 = lst_path[0]
    path_2 = lst_path[1]
    if vector == vector_all_one_two:
        syn_all_newer_on_noprefix_file____one(file_newer_in_one, path_1, path_2, delimetr_main)
        syn_all_newer_on_noprefix_file____two(file_newer_in_two, path_1, path_2, delimetr_main)
    elif vector == vector_one_in_two:
        syn_all_newer_on_noprefix_file____one(file_newer_in_one, path_1, path_2, delimetr_main)
    elif vector == vector_two_in_one:
        syn_all_newer_on_noprefix_file____two(file_newer_in_two, path_1, path_2, delimetr_main)
    else:
        print(no_recognized)
def syn_all_newer_on_noprefix_file____one(file_newer_in_one, path_1, path_2, delimetr_main):
    for fnio in file_newer_in_one:
        temp_file_one_path_1_from = path_1 + fnio
        temp_file_one_path_2_to = path_2 + fnio
        copy_and_replace_file(temp_file_one_path_1_from, temp_file_one_path_2_to, delimetr_main)
def syn_all_newer_on_noprefix_file____two(file_newer_in_two, path_1, path_2, delimetr_main):
    for fnit in file_newer_in_two:
        temp_file_two_path_2_from = path_2 + fnit
        temp_file_two_path_1_to = path_1 + fnit
        copy_and_replace_file(temp_file_two_path_2_from, temp_file_two_path_1_to, delimetr_main)


def add_unique_noprefix_file(file_only_in_one, file_only_in_two, lst_path, vector, delimetr_main):
    path_1 = lst_path[0]
    path_2 = lst_path[1]
    if vector == vector_all_one_two:
        add_unique_noprefix_file____from_one(file_only_in_one, path_1, path_2, delimetr_main)
        add_unique_noprefix_file____from_two(file_only_in_two, path_1, path_2, delimetr_main)
    elif vector == vector_one_in_two:
        add_unique_noprefix_file____from_one(file_only_in_one, path_1, path_2, delimetr_main)
    elif vector == vector_two_in_one:
        add_unique_noprefix_file____from_two(file_only_in_two, path_1, path_2, delimetr_main)
    else:
        print(no_recognized)
def add_unique_noprefix_file____from_one(file_only_in_one, path_1, path_2, delimetr_main):
    for foio in file_only_in_one:
        temp_file_one_path_1_from = path_1 + foio
        temp_file_one_path_2_to = path_2 + foio
        copy_unique_noprefex_file(temp_file_one_path_1_from, temp_file_one_path_2_to, delimetr_main)
def add_unique_noprefix_file____from_two(file_only_in_two, path_1, path_2, delimetr_main):
    for foit in file_only_in_two:
        temp_file_two_path_2_from = path_2 + foit
        temp_file_two_path_1_to = path_1 + foit
        copy_unique_noprefex_file(temp_file_two_path_2_from, temp_file_two_path_1_to, delimetr_main)

def add_new_frefix_file(file_newer_in_one, file_newer_in_two, lst_path, vector, delimetr_main):
    path_1 = lst_path[0]
    path_2 = lst_path[1]
    if vector == vector_all_one_two:
        add_new_frefix_file____one(file_newer_in_one, path_1, path_2, delimetr_main)
        add_new_frefix_file____two(file_newer_in_two, path_1, path_2, delimetr_main)
    elif vector == vector_one_in_two:
        add_new_frefix_file____one(file_newer_in_one, path_1, path_2, delimetr_main)
    elif vector == vector_two_in_one:
        add_new_frefix_file____two(file_newer_in_two, path_1, path_2, delimetr_main)
    else:
        print(no_recognized)
def add_new_frefix_file____one(file_newer_in_one, path_1, path_2, delimetr_main):
    for fnio in file_newer_in_one:
        temp_file_one_path_1_from = path_1 + fnio
        temp_file_one_path_2_to = path_2 + fnio
        copy_add_new_prefex_file(temp_file_one_path_1_from, temp_file_one_path_2_to, delimetr_main)
def add_new_frefix_file____two(file_newer_in_two, path_1, path_2, delimetr_main):
    for fnit in file_newer_in_two:
        temp_file_two_path_2_from = path_2 + fnit
        temp_file_two_path_1_to = path_1 + fnit
        copy_add_new_prefex_file(temp_file_two_path_2_from, temp_file_two_path_1_to, delimetr_main)

def replace_all_prefix_file_of_one(file_newer_in_one, file_newer_in_two, lst_path, vector, delimetr_main):
    path_1 = lst_path[0]
    path_2 = lst_path[1]
    if vector == vector_all_one_two:
        replace_all_prefix_file_of_one____one(file_newer_in_one, path_1, path_2, delimetr_main)
        replace_all_prefix_file_of_one____two(file_newer_in_two, path_1, path_2, delimetr_main)
    elif vector == vector_one_in_two:
        replace_all_prefix_file_of_one____one(file_newer_in_one, path_1, path_2, delimetr_main)
    elif vector == vector_two_in_one:
        replace_all_prefix_file_of_one____two(file_newer_in_two, path_1, path_2, delimetr_main)
    else:
        print(no_recognized)
def replace_all_prefix_file_of_one____one(file_newer_in_one, path_1, path_2, delimetr_main):
    for fnio in file_newer_in_one:
        temp_file_one_path_1_from = path_1 + fnio
        temp_file_one_path_2_to = path_2 + fnio
        copy_and_replace_all_prefix_file(temp_file_one_path_1_from, temp_file_one_path_2_to, delimetr_main)
def replace_all_prefix_file_of_one____two(file_newer_in_two, path_1, path_2, delimetr_main):
    for fnit in file_newer_in_two:
        temp_file_two_path_2_from = path_2 + fnit
        temp_file_two_path_1_to = path_1 + fnit
        copy_and_replace_all_prefix_file(temp_file_two_path_2_from, temp_file_two_path_1_to, delimetr_main)


def main():
    print(start_or_quit)
    inp = input()
    if inp == start_number:
        while inp != quit:
            print(watch_all_or_analys_or_quit)
            inp = input()
            if inp == start_number:
                lst_path, delimetr = input_paths()
                print_files(get_full_files_of_all_pasths(lst_path, delimetr))                
            if inp == analys_number: 
                lst_path, delimetr = input_paths()
                (file_only_in_one, file_only_in_two, file_newer_in_one, file_newer_in_two, file_which_in_one_and_in_two, lst_path) = syncronize(get_full_files_of_all_pasths(lst_path, delimetr), lst_path, delimetr)
                inp_2 = ""
                while inp_2 != quit:
                    print_sync_info()
                    inp_2 = input()
                    if inp_2 == quit:
                        break
                    inp_2_list = inp_2.split(" ")
                    for l in inp_2_list:
                        try:
                            action = l.split("-")[0]
                            vector = l.split("-")[1]
                        except:
                            print(uncorrent_write)
                            continue
                        if (action not in action_examination) or (vector not in vector_examination):
                            print(uncorrent_write)
                            break
                    for l in inp_2_list:
                        try:
                            action = l.split("-")[0]
                            vector = l.split("-")[1]
                        except:
                            print(uncorrent_write)
                            continue
                        if action == action_one:
                            syn_all_newer_on_noprefix_file(file_newer_in_one, file_newer_in_two, lst_path, vector, delimetr)
                        if action == action_two:
                            add_unique_noprefix_file(file_only_in_one, file_only_in_two, lst_path, vector, delimetr)
                        if action == action_three:
                            add_new_frefix_file(file_newer_in_one, file_newer_in_two, lst_path, vector, delimetr)
                        if action == action_four:
                            replace_all_prefix_file_of_one(file_newer_in_one, file_newer_in_two, lst_path, vector, delimetr)
                        
            if inp == quit:
                break
    elif inp == quit:
        raise SystemExit(1)
    else:
        print(uncorrent_write)

if __name__ == "__main__":
    main()



