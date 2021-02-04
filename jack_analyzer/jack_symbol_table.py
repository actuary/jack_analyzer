

class JackSymbolNotFound(Exception):
    pass

class SymbolTable(object):

    def __init__(self):
        # name, type, kind
        table = []

    def define(**new_row):
        table.append(new_row)

    def var_count(kind):
        return sum(row["kind"]==kind for row in table)

    def kind_of(name):
        for row in table:
            if row["name"]==name:
                return row["kind"]

        raise JackSymbolNotFound
    
    def type_of(name):
        for row in table:
            if row["name"]==name:
                return row["kind"]

        raise JackSymbolNotFound

    def index_of(self, name):
        for i, row in enumerate(table):
            if row["name"]==name:
                return i

        raise JackSymbolNotFound

            
    
