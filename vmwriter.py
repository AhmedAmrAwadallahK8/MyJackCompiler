
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

    :param kind: (String) Kind of memory segment
    :param index: (String) Allocated memory index
    :return: (String) VM Translation
    """
    vm_out = 'pop ' + kind + ' ' + index + '\n'
    return vm_out

    ops = ('+', '-', '*', '/', '&gt;', '&lt;', '=', '|', '&amp;')
    unary_ops = ('-', '~')
def write_arithmetic(op=None, unary_op=None):
    """VM op code

    :param op: (String) Op symbol
    :param unary_op: (String) Unary op symbol
    :return: (String) VM Translation
    """
    vm_out = ''
    if op:
        if op == '+':
            vm_out += 'add\n'
        elif op == '-':
            vm_out += 'sub\n'
        elif op == '*':
            vm_out += 'call Math.multiply 2\n'
        elif op == '/':
            vm_out += 'call Math.divide 2\n'
        elif op == '>':
            vm_out += 'gt\n'
        elif op == '<':
            vm_out += 'lt\n'
        elif op == '=':
            vm_out += 'eq\n'
        elif op == '|':
            vm_out += 'or\n'
        elif op == '&':
            vm_out += 'and\n'
    elif unary_op:
        if op == '-':
            vm_out += 'neg\n'
        elif op == '~':
            vm_out += 'not\n'
    return vm_out


def write_label(l_name):
    """VM label code

    :param l_name: (String) Unique label name
    :return: VM Translation
    """
    vm_out = 'label ' + l_name + '\n'
    return vm_out


def write_goto(tar_label):
    """VM unconditional goto code

    :param tar_label: (String) Label to jump to
    :return: (String) VM Translation
    """
    vm_out = 'goto ' + tar_label + '\n'
    return vm_out


def write_if(tar_label):
    """VM conditional goto code

    :param tar_label: (String) Label to jump to
    :return: (String) VM Translation
    """
    vm_out = 'if-goto ' + tar_label + '\n'
    return vm_out


def write_call(class_name, subroutine_name, num_args):
    """VM function call code

    :param class_name: (String) name of class subroutine belongs to
    :param subroutine_name: (String) name of subroutine
    :param num_args: (int) number of arguments the function requires
    :return: (String) VM Translation
    """
    vm_out = 'call ' + class_name + '.' + subroutine_name + ' ' + num_args + '\n'
    return vm_out


def write_function(class_name, subroutine_name, num_vars):
    """VM function initialization code

    :param class_name: (String) name of class subroutine belongs to
    :param subroutine_name: (String) name of subroutine
    :param num_vars: (int) number of variables the function requires
    :return: (String) VM Translation
    """
    vm_out = 'function ' + class_name + '.' + subroutine_name + ' ' + num_vars + '\n'
    return vm_out


def write_return():
    """VM return code

    :return: VM Translation
    """
    vm_out = 'return\n'
    return vm_out
