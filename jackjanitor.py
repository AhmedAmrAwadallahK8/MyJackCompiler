
def clean_jack_code(jack_code):
    """Takes in a List of Strings and removes all endlines and Jack comment lines from it

    :param jack_code: (List) List of Strings
    :return: (List) List of Strings
    """
    endline_jack_code = []
    cleaned_jack_code = []
    t2_comment_found = False
    # Remove endlines
    for line in jack_code:
        endline_ind = line.find('\n')
        if endline_ind != -1:
            endline_jack_code.append(line[:endline_ind])

    # Remove Comments
    for line in endline_jack_code:
        comment_ind_t1 = line.find('//')
        comment_ind_t2_s = line.find('/**')
        comment_ind_t2_e = line.find('*/')
        # Remove Comments
        if comment_ind_t1 == -1 and comment_ind_t2_s == -1 and comment_ind_t2_e == -1 and not t2_comment_found:
            cleaned_jack_code.append(line)
        elif comment_ind_t1 == 0:
            pass
        elif comment_ind_t1 != -1:
            cleaned_jack_code.append(line[:comment_ind_t1])
        # Start of a type two comment is found or was found in a previous line
        elif comment_ind_t2_s != -1 or t2_comment_found:
            t2_comment_found = True
            # The type 2 comment starts and ends in the same line
            if comment_ind_t2_e != -1 and comment_ind_t2_s != -1:
                # If the end of the comment is not the end of the line then append the rest of the line
                if comment_ind_t2_e+2 != len(line):
                    cleaned_jack_code.append(line[comment_ind_t2_e+2:])
                t2_comment_found = False
            # The type 2 comment start is not in this line but a comment end is in this line
            elif comment_ind_t2_e != -1 and comment_ind_t2_s == -1:
                # If the end of the comment is not the end of the line then append the rest of the line
                if comment_ind_t2_e+2 != len(line):
                    cleaned_jack_code.append(line[comment_ind_t2_e+2:])
                t2_comment_found = False
    return cleaned_jack_code


