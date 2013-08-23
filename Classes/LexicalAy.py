__author__ = 'Matheus'


class LexicalAy(object):

    # Constructor
    def __init__(self, symtable):
        # Attributes initialization
        """

        :param symtable:
        """
        self.token = ""
        self.previousToken = ""
        self.lineNumber = 1
        self.line = ""
        self.symtable = symtable

    def getToken(self, line):
        # Retrieves the next token in current line and stores in token attribute, insert it in the symbol table
        """

        :param line:
        """
        global keywords, symbols

        # TODO - Automaton implementation for token recognition