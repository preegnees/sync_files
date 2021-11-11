# importing the modules
import os
import shutil 
import datetime as dt


def _time_now():
    date = dt.datetime.now()
    return str(date.year) + "-" + str(date.month) + "-" + str(date.day) + "-" + str(date.hour) + "-" + str(date.minute) + "-" + str(date.second)


def copy_and_replace_file(from_file, to_file, delimetr_main):
    delimetr_main = delimetr_main[0]
    print("copy_and_replace_file")
    prefix = "--radmir_3000--"
    file_name_to = to_file.split(delimetr_main)[-1]

    dir_to = to_file.split(delimetr_main)[0:-1]

    to = delimetr_main.join(dir_to) + delimetr_main + prefix + file_name_to
    fr = from_file
    to_replace = to.replace(prefix, "")

    try:
        shutil.copy(fr, to) 
        shutil.copystat(fr, to)
        os.remove(to_replace)
        shutil.move(to, to_replace)
        shutil.copystat(fr, to_replace)
    except:
        os.remove(to)
        print("похоже, что в папке, куда идет замены нету файла ", fr, ", которого нужно заменить [*-*]")



def copy_add_new_prefex_file(from_file, to_file, delimetr_main):
    delimetr_main = delimetr_main[0]
    prefix = "--radmir--"
    time = _time_now()
    file_name_to = to_file.split(delimetr_main)[-1]

    dir_to = to_file.split(delimetr_main)[0:-1]

    to = delimetr_main.join(dir_to) + delimetr_main + time + prefix + file_name_to
    fr = from_file
    shutil.copy(fr, to) 
    shutil.copystat(fr, to)


def copy_and_replace_all_prefix_file(from_file, to_file, delimetr_main):
    delimetr_main = delimetr_main[0]
    prefix = "--radmir--"
    time = _time_now()

    file_name_to = to_file.split(delimetr_main)[-1]

    dir_to = to_file.split(delimetr_main)[0:-1]
    dir_to_join = delimetr_main.join(dir_to)

    to = delimetr_main.join(dir_to) + delimetr_main + time + prefix + file_name_to
    fr = from_file


    lst_files = os.listdir(dir_to_join)
    for l in lst_files:
        if (prefix + file_name_to) in l:
            os.remove(dir_to_join + delimetr_main + l)
    shutil.copy(fr, to) 
    shutil.copystat(fr, to)


def copy_unique_noprefex_file(from_file, to_file, delimetr_main):
    delimetr_main = delimetr_main[0]
    file_name_to = to_file.split(delimetr_main)[-1]

    dir_to = to_file.split(delimetr_main)[0:-1]

    to = delimetr_main.join(dir_to) + delimetr_main + file_name_to
    fr = from_file
    shutil.copy(fr, to) 
    shutil.copystat(fr, to)