__author__ = 'Matheus'
__author__ = 'Rafael'
__author__ = 'Thiago'


class SymTable(object):
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

    def printTable(self):
        for e, (name, klass, ttype, scope, value, linedc, lineref) in self.table.items():
            print("[{0}] -({1} - {2} - {3} - {4} - {5} - {6} - {7})".format(e, name, klass, ttype, scope, value, linedc, lineref))

    def insertSymbol(self, key, stuff):
        self.table[key] = stuff

    def removeSymbol(self, key):
        self.table.pop(key)