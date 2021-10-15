import sys
import os


def extract_file(file_name):
    """ Takes a file and returns a list of its contents

    :param file_name: (String) Name of file
    :return: (List) made up of all the lines of text within the file
    """
    file_contents = []
    with open(file_name, 'r') as f:
        for line in f:
            file_contents.append(line)
    return file_contents


def extract_folder(folder_name):
    """

    :param folder_name: (String) Name of folder
    :return: (Dictionary) Folders Path and List of files
    """
    origin_path = os.getcwd()
    folder_path = origin_path + '/' + folder_name
    os.chdir(folder_path)
    file_list = os.listdir()
    os.chdir(origin_path)
    return {"path": folder_path, "files": file_list}


output = extract_file('testtext.txt')
print(output)
print(os.getcwd())
output = extract_folder('testdirec')
print(output)
print(os.getcwd())




