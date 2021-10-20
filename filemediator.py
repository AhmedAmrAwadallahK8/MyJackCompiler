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
    """ Takes a folder and reports its path and the list of files within the folder

    :param folder_name: (String) Name of folder
    :return: (Dictionary) Folders Path and List of files
    """
    origin_path = os.getcwd()
    folder_path = origin_path + '/' + folder_name
    os.chdir(folder_path)
    file_list = os.listdir()
    os.chdir(origin_path)
    return {"path": folder_path, "files": file_list}


def load_file(file_name, file_type, data, folder_name=''):
    """ Creates a new file that contains the input data. File extension needs to be specified. If the transformed file
        came from a directory it will be return to the specified directory. The directory has to be in the current
        working directory.

    :param file_name: (String) Name of the file
    :param file_type: (String) File extension
    :param data: (String) Data to be put into the file
    :param folder_name: (String) Name of the directory in the current working directory.
    :return:
    """
    origin_path = ''
    folder_path = ''
    if folder_name != '':
        origin_path = os.getcwd()
        folder_path = origin_path + '/' + folder_name
        os.chdir(folder_path)

    file = file_name + file_type
    with open(file, 'w') as f:
        f.write(data)

    if folder_name != '':
        os.chdir(origin_path)


