
class SymbolTable:
    def __init__(self, parent_table=None):
        self.parent_table = parent_table
        self.sub_table = SymbolTable(self)

    # TODO resets sub_table
    def start_subroutine(self):
        pass

    # TODO defines a new variable and all relevent information
    def define(self):
        pass

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
