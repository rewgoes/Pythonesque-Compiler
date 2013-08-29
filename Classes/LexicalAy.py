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
        self.scope = 1
        self.symtable = symtable

    def getToken(self, line, strerr=None, plist=None):
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

        # Strip tab keys since they're not a problem in this language
        #line = line.replace('\t', ' ')

        # Format of symboltable [ KEY, (NAME, CLASS, TYPE, SCOPE, VALUE, LINE DECLARED, LINE REFERENCED) ]

        self.lineNumber += 1

        if plist:
            self.listToken = list
        else:
            self.listToken = []

        if strerr:
            auto = 'string_error'
            self.lineNumber -= 1
        else:
            auto = 'begin'

        state = 0
        tmp = ''

        for c in line:
            # String automaton
            # TODO - Fix recognition when there's tokens before a string open and this string doesn't close, causing a strerror automaton
            # What's happening basically: When automaton reads " it enters the string sub-automaton. Then it will read any characters expect \n.
            # If it finds a closing quote it will append the token to the listToken, otherwise if it never finds the closing quote, it will treat
            # this as a string_error, which will trigger another call to this function to retrieve the tokens that weren't retrieved the first time
            # because it was being treated as a string. But, the problem is that if there's token BEFORE and opening quote, it will append these twice.
            if auto == 'string':
                if state == 1 and c != '"':
                    if c == '\n':
                        auto = 'string_error'
                    else:
                        tmp += c
                elif state == 1 and c == '"':
                    state = 2
                    tmp += c

                if state == 2:
                    self.listToken.append(Token(tmp, 'cadeia_literal'))
                    auto = 'begin'
                    continue

            # Comment automaton
            if auto == 'comment':
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
                if state == 1:
                    if c.isdigit():
                        tmp += c
                    elif not c.isdigit():
                        if c == '.':
                            state = 2
                        else:
                            self.listToken.append(Token(tmp, 'numero_inteiro'))
                            auto = 'begin'

                if state == 2:
                    if c == '.':
                        state = 3
                        continue

                if state == 3:
                    if c.isdigit():
                        tmp += '.'
                        state = 4
                    elif c == '.':
                        self.listToken.append(Token(tmp, 'numero_inteiro'))
                        self.listToken.append(Token('..', '..'))
                        auto = 'begin'
                        continue
                    else:
                        self.listToken.append(Token(tmp, 'numero_inteiro'))
                        self.listToken.append(Token('.', '.'))
                        auto = 'begin'

                if state == 4:
                    if c.isdigit():
                        tmp += c
                    else:
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
                if state == 1 and (c.isalnum() or c == '_'):
                    tmp += c
                    state = 2
                elif state == 1 and (not c.isalnum() or c != '_'):
                    state = 2
                elif state == 2 and (c.isalnum() or c == '_'):
                    tmp += c

                if state == 2 and not (c.isalnum() or c == '_'):
                    if tmp in self.symtable.table:
                        if self.symtable.table[tmp][2] == 'identificador':
                            self.listToken.append(Token(tmp, 'identificador'))
                        else:
                            self.listToken.append(Token(tmp, tmp))
                    else:
                        self.symtable.insertSymbol(tmp, (tmp, 'variavel', 'identificador', self.scope, 'null', self.lineNumber, self.lineNumber))
                        self.listToken.append(Token(tmp, 'identificador'))
                    auto = 'begin'

            # String Error
            if auto == 'string_error':
                if not strerr:
                    self.listToken = self.getToken(line, strerr=True, plist=self.listToken)
                    return self.listToken
                else:
                    if state == 0 and c == '"':
                        tmp += c
                        self.listToken.append(Token('Linha ' + str(self.lineNumber) + ': ' + tmp, 'simbolo nao identificado'))
                        auto = 'begin'
                        continue

            # Checks which automaton to enter
            if auto == 'begin':
                tmp = ''
                state = 1
                if c == '\t':
                    continue
                if c == '"':
                    tmp += c
                    auto = 'string'
                elif c == '{':
                    auto = 'comment'
                elif c.isdigit():
                    tmp += c
                    auto = 'number'
                elif not c.isalnum() and c != '\n' and c != ' ' and c != '_':
                    tmp += c
                    auto = 'symbol'
                    openq = True
                    closeq = False
                elif (c.isalpha() or c == '_') and c != '\n' and c != ' ':
                    tmp += c
                    auto = 'names'

        return self.listToken