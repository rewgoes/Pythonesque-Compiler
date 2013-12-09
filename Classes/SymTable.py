__author__ = 'Bruno_Matheus_Rafael_Thiago'


class SymTable(object):
    # Constructor
    def __init__(self, keywords, keysymbols):
        self.table = self.initTable(keywords, keysymbols)
        self.local = []

    def initTable(self, keywords, keysymbols):
        # Format of symboltable [ KEY, (NAME, TOKEN, CATEGORY, TYPE, VALUE, SCOPE, PARAM) ]
        tmp = {}

        # TODO - Review the following lines
        for e in keysymbols:
            tmp[e] = {'name': e, 'token': "res", 'category': "symbol", 'type': 0, 'value': e, 'scope': 0, 'param': []}

        for e in keywords:
            tmp[e] = {'name': e, 'token': "res", 'category': e, 'type': 0, 'value': e, 'scope': 0, 'param': []}

        return tmp

    # Prints the Symbol Table
    def printTable(self):
        for e, (name, token, category, ttype, value, scope) in self.table.items():
            print("[{0}] -({1} - {2} - {3} - {4} - {5} - {6})".format(e, name, token, category, ttype, value, scope))

    # Insert a symbol in the table
    def insertSymbol(self, key, stuff):
        if key in self.table:
            return False
        else:
            self.table[key] = {}
            self.table[key]['name'] = stuff[0]
            self.table[key]['token'] = stuff[1]
            self.table[key]['category'] = stuff[2]
            self.table[key]['type'] = stuff[3]
            self.table[key]['value'] = stuff[4]
            self.table[key]['scope'] = stuff[5]
            if self.table[key]['scope'] == 'local':
                self.local.append(key)
            self.table[key]['param'] = stuff[6]
            return True

    # Removes a symbol from the table
    def removeSymbol(self, key):
        self.table.pop(key)
        
    def removeLocal(self):
        for key in self.local:
            self.table.pop(key)
