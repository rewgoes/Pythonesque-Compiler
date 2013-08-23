from Classes.Token import Token

__author__ = 'Matheus'


class LexicalAy(object):

    # Constructor
    def __init__(self, symtable):
        # Attributes initialization
        """

        :param symtable:
        """
        self.listToken = []
        self.previousToken = ""
        self.lineNumber = 0
        self.line = ""
        self.scope = 1
        self.symtable = symtable

    def getToken(self, line):
        # Retrieves the next token in current line and stores in token attribute
        """

        :param line:
        """
        global keywords, symbols
        # TODO - Automaton implementation for token recognition
        # RegExes:
        # ID: [a-zA-Z_]+[0-9a-zA-Z_]*
        # Comments: {.*}
        # Integers: [0-9]+
        # Float: [0-9]+\.[0-9]+
        # Strings: "[^"]+"

        self.lineNumber += 1
        self.listToken = []
        auto = "begin"
        state = 0
        tmp = ""

        for c in line:
            # String automaton
            if auto == "string":
                if state == 1 and c != '"':
                    if c == '\n':
                        self.listToken.append(Token('Linha ' + str(self.lineNumber) + ': ', 'cadeia nao fechada', True))
                        auto = 'begin'
                        continue
                    tmp += c
                elif state == 1 and c == '"':
                    state = 2
                    tmp += c

                if state == 2:
                    self.listToken.append(Token(tmp, 'cadeia_literal'))
                    auto = "begin"
                    continue

            # Comment automaton
            if auto == "comment":
                if state == 1 and c != '}':
                    if c == '\n':
                        self.listToken.append(Token('Linha ' + str(self.lineNumber) + ': ', 'comentario nao fechado', True))
                        auto = 'begin'
                        continue
                if state == 1 and c == '}':
                    auto = 'begin'
                    continue

            # Number automaton
            if auto == 'number':
                if state == 1 and c.isdigit():
                    tmp += c
                elif state == 1 and not c.isdigit():
                    if c == '.':
                        state = 2
                        tmp += c
                    elif c == '\n' or c == ' ':
                        self.listToken.append(Token(tmp, 'numero_inteiro'))
                        auto = 'begin'
                elif state == 2 and c.isdigit():
                    tmp += c
                elif state == 2 and not c.isdigit():
                    if c == '\n':
                        self.listToken.append(Token(tmp, 'numero_real'))
                        auto = 'begin'

            # Symbols
            if auto == 'symbol':
                    if tmp+c in self.symtable.table:
                        tmp += c
                    elif tmp in self.symtable.table:
                        self.listToken.append(Token(tmp, tmp))
                        auto = 'begin'
                    else:
                        self.listToken.append(Token('Linha ' + str(self.lineNumber) + ': ' + tmp, 'simbolo nao identificado'))
                        auto = 'begin'

            # Names
            if auto == 'names':
                if state == 1 and (c.isalpha() or c == '_'):
                    tmp += c
                    state = 2
                elif state == 2 and (c.isalnum() or c == '_'):
                    tmp += c
                if state == 2 and not (c.isalnum() or c == '_'):
                    if tmp in self.symtable.table:
                        self.listToken.append(Token(tmp, tmp))
                    else:
                        self.listToken.append(Token(tmp, 'identificador'))
                    auto = 'begin'

            # Checks which automaton to enter
            if auto == "begin":
                tmp = ""
                state = 1
                if c == '"':
                    tmp += c
                    auto = "string"
                elif c == '{':
                    auto = "comment"
                elif c.isdigit():
                    tmp += c
                    auto = 'number'
                elif not c.isalnum() and c != '\n' and c != ' ':
                    tmp += c
                    auto = 'symbol'
                elif (c.isalpha() or c == '_') and c != '\n' and c != ' ':
                    tmp += c
                    auto = 'names'

        return self.listToken