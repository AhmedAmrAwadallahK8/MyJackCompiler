
def write_push(kind, index):
    """VM push command code

    :param kind: Kind of memory segment
    :param index: Allocated memory index
    :return: (String) VM Translation
    """
    vm_out = 'push ' + kind + ' ' + index + '\n'
    return vm_out


def write_pop(kind, index):
    """VM pop command code

    :param kind: Kind of memory segment
    :param index: Allocated memory index
    :return: (String) VM Translation
    """
    vm_out = 'pop ' + kind + ' ' + index + '\n'
    return vm_out

    ops = ('+', '-', '*', '/', '&gt;', '&lt;', '=', '|', '&amp;')
    unary_ops = ('-', '~')
def write_arithmetic(op=None, unary_op=None):
    if op:
        of
    pass


def write_label():
    pass


def write_goto():
    pass


def write_if():
    pass


def write_call():
    pass


def write_function():
    pass


def write_return():
    pass
