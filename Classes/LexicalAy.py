__author__ = 'Matheus'

class LexicalAy(object):

    # Constructor
    def __init__(self, ktable):
        # Attributes initialization
        self.token = ""
        self.previousToken = ""
        self.lineNumber = 1
        self.line = ""
        self.table = ktable

    def getToken(self, line):
        # Retrieves the next token in current line and stores in token attribute
        global keywords, symbols

        # TODO - Automaton implementation for token recognition