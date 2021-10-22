
class SymbolTable:
    def __init__(self, class_table=None):
        self.table = {}
        self.kind_count = {'local': 0, 'argument': 0, 'this': 0, 'that': 0, 'static': 0}
        self.class_table = class_table
        if class_table is None:
            self.sub_table = SymbolTable(self)

    def get_sub(self):
        return self.sub_table

    # TODO resets sub_table
    def start_subroutine(self):
        """Resets the state of the subroutine symbol table to default

        :return: None
        """
        self.sub_table.table = {}
        for k in self.sub_table.kind_count:
            self.sub_table.kind_count[k] = 0

    # TODO defines a new variable and all relevent information
    def define(self, name, j_type, kind):
        """Updates the symbol table with a new variable

        :param name: Identifier name in code
        :param j_type: Jack code type of variable
        :param kind: The kind of memory segment it belongs to in vm code
        :return: None
        """
        self.table[name] = (j_type, kind, self.kind_count[kind])
        self.kind_count[kind] += 1

    # TODO returs number of given kind of variable in scope
    def var_count(self):
        pass

    # TODO returns kind of named identifier in current scope
    def kind_of(self):
        pass

    # TODO returns type of named identifier in current scope
    def type_of(self):
        pass

    # TODO returns the index assigned to the named identifier
    def index_of(self):
        pass


a = SymbolTable()
b = a.get_sub()
