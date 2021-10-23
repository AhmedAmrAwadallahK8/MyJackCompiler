
class SymbolTable:
    def __init__(self, parent_table=None):
        self.table = {}
        self.kind_count = {'static': 0, 'field': 0, 'argument': 0, 'var': 0}
        self.parent_table = parent_table

    def start_subroutine(self):
        """Resets the state of the subroutine symbol table to default

        :return: (SymbolTable) A SymbleTable object that is will have a link to the SymbolTable that called this method
        """
        return SymbolTable(self)

    def define(self, name, j_type, kind):
        """Updates the symbol table with a new variable

        :param name: Identifier name in code
        :param j_type: Jack code type of variable
        :param kind: The kind of memory segment it belongs to in vm code
        :return: None
        """
        self.table[name] = (j_type, kind, self.kind_count[kind])
        self.kind_count[kind] += 1

    def var_count(self, kind):
        """

        :param kind: VM memory segment kind
        :return: (int) Number of times the memory segment has been defined in scope
        """
        return self.kind_count[kind]

    # TODO This function is not complete must be able to handle situations where the identifier is unknown in scope
    def kind_of(self, name):
        """For a given variable name return its kind

        :param name: (String) name of variable
        :return: (String) the variables's kind
        """
        if name in self.table.keys():
            return self.table[name][1]
        else:
            return None

    def type_of(self, name):
        """For a given variable name return its type

        :param name: (String) name of variable
        :return: (String) the variable's type
        """
        return self.table[name][0]

    def index_of(self, name):
        """For a given variable name return the memory index based on its kind

        :param name: (String) name of variable
        :return: (int) the index in memory allocated for this variable
        """
        return self.table[name][2]


'''a = SymbolTable()
b = a.start_subroutine()
a.define('x', 'int', 'argument')
print(a.table)
print(a.var_count('argument'))
print(a.kind_of('x'))
print(a.type_of('x'))
print(a.index_of('x'))
b.define('y', 'int', 'argument')
print(b.table)
print(b.kind_count)
b = a.start_subroutine()
print(b.table)
print(b.kind_count)'''
