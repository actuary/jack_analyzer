

class JackSymbolNotFound(Exception):
    pass

class SymbolTable(object):

    def __init__(self):
        # name, type, kind, index
        self.table = []

    def define(self, new_row, starting_index = 0):        
        new_row["index"] = self.var_count(new_row["kind"])
        self.table.append(new_row)

    def var_count(self, kind):
        return sum([row["kind"]==kind for row in self.table])

    def kind_of(self, name):
        for row in self.table:
            if row["name"]==name:
                return row["kind"]

        raise JackSymbolNotFound
    
    def type_of(self, name):
        for row in self.table:
            if row["name"]==name:
                return row["type"]

        raise JackSymbolNotFound

    def index_of(self, name):
        for i, row in enumerate(self.table):
            if row["name"]==name:
                return row["index"]

        raise JackSymbolNotFound
    def exists(self, name):
        for row in self.table:
            if row["name"] == name:
                return True

        return False
    
