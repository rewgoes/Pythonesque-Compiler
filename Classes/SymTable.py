__author__ = 'Bruno_Matheus_Rafael_Thiago'


class SymTable(object):
    # Constructor
    def __init__(self, keywords, keysymbols):
        self.table = self.initTable(keywords, keysymbols)

    def initTable(self, keywords, keysymbols):
        # Format of symboltable [ KEY, (NAME, TOKEN, CATEGORY, TYPE, VALUE, SCOPE) ]
        tmp = dict()

        # TODO - Review the following lines
        for e in keysymbols:
            tmp[e] = (e, "res", "symbol", 0, e, 0)

        for e in keywords:
            tmp[e] = (e, "res", e, 0, e, 0)

        return tmp

    # Prints the Symbol Table
    def printTable(self):
        for e, (name, token, category, ttype, value, scope) in self.table.items():
            print("[{0}] -({1} - {2} - {3} - {4} - {5} - {6})".format(e, name, token, category, ttype, value, scope))

    # Insert a symbol in the table
    def insertSymbol(self, key, stuff):
        self.table[key] = stuff

    # Removes a symbol from the table
    def removeSymbol(self, key):
        self.table.pop(key)