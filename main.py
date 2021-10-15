import sys
import os
import filemediator as fm


def folder_test(file_name):
    """Tests if the input file is a directory

    :param file_name: (String) Name of file
    :return: (Boolean) Returns true if the file is a directory else false
    """
    origin_path = os.getcwd()
    file_path = origin_path + '/' + file_name
    return os.path.isdir(file_path)

def jack_test(file_name):
    """Tests if the input file is a jack file

    :param file_name: (String) Name of file
    :return: (Boolean) True if the file is a jack file otherwise false
    """
    jack_ext = file_name.find('.jack')
    if jack_ext == -1:
        return False
    else:
        return True

def extract_folder_files(folder_name):
    """Extract all data from the jack files in a directory

    :param folder_name: (String) Name of folder
    :return: (List) List of lines of all jack code present in every file
    """
    jack_code = []
    folder_info = fm.extract_folder(folder_name)
    file_list = folder_info['files']
    origin_direc = os.getcwd()
    os.chdir(folder_info['path'])
    for file in file_list:
        if jack_test(file):
            jack_code = jack_code + fm.extract_file(file)
    os.chdir(origin_direc)
    return jack_code



def main(sys_input):
    jack_code = []
    is_folder = folder_test(sys_input)
    if is_folder:
        pass


    return













#input = sys.argv[1]
#main(input)

