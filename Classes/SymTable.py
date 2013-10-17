__author__ = 'Matheus'
__author__ = 'Rafael'
__author__ = 'Thiago'
__author__ = 'Bruno'


class SymTable(object):
    # Constructor
    def __init__(self, keywords, keysymbols):
        self.table = self.initTable(keywords, keysymbols)

    def initTable(self, keywords, keysymbols):
        # Format of symboltable [ KEY, (NAME, CLASS, TYPE, SCOPE, VALUE, LINE DECLARED, LINE REFERENCED) ]
        tmp = dict()

        # TODO - Review the following lines
        for e in keysymbols:
            tmp[e] = (e, "res", "symbol", 0, e, 0, 0)

        for e in keywords:
            tmp[e] = (e, "res", e, 0, e, 0, 0)

        return tmp

    # Prints the Symbol Table
    def printTable(self):
        for e, (name, klass, ttype, scope, value, linedc, lineref) in self.table.items():
            print("[{0}] -({1} - {2} - {3} - {4} - {5} - {6} - {7})".format(e, name, klass, ttype, scope, value, linedc, lineref))

    # Insert a symbol in the table
    def insertSymbol(self, key, stuff):
        self.table[key] = stuff

    # Removes a symbol from the table
    def removeSymbol(self, key):
        self.table.pop(key)