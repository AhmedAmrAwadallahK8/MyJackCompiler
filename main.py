import sys
import os
import filemediator as fm


def folder_test(file_name):
    """

    :param file_name: (String) Name of file
    :return: (Boolean) Returns true if the file is a directory else false
    """
    origin_path = os.getcwd()
    file_path = origin_path + '/' + file_name
    return os.path.isdir(file_path)


def main(sys_input):

    return
















#input = sys.argv[1]
#main(input)

