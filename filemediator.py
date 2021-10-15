import sys
import os


def extract_file(file_name):
    """Takes a file and returns a list of its contents

        Parameters:
        file_name (String): Name of file

        Returns:
        list: List made up of all the lines of text within the file

    """
    file_contents = []
    with open(file_name, 'r') as f:
        for l in f:
            file_contents.append(l)
    return file_contents

def extract_folder(folder_name):
    return


output = extract('testtext')
print(output)




