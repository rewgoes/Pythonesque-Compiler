__author__ = 'Matheus_Rafael_Thiago_Bruno'

from Classes.Token import Token
import linecache


class LexicalAy(object):
    # Constructor
    def __init__(self, symtable, file, error):
        # Attributes initialization
        """
        :param symtable: Symbol table class object reference
        :param file: path to the input file, not opened
        :param error: Error class object reference
        """
        self.file = file

        # Initialisation of class attributes
        # Line to be analyzed
        self.line = ''

        # List of tokens found on line
        self.listToken = []

        # List of error messages
        self.listMessage = []

        # Reference to Error class
        self.errorRef = error

        # Current lineNumber
        self.lineNumber = 0

        # Current scope
        self.scope = 1

        # Reference do SymTable class
        self.symtable = symtable

    def getToken(self, strerr=None, plist=None):
        # Retrieves the next token in current line and stores in token attribute

        global keywords, symbols
        # RegExes:
        # ID: [a-zA-Z_]+[0-9a-zA-Z_]*
        # Comments: {.*}
        # Integers: [0-9]+
        # Float: [0-9]+\.[0-9]+
        # Strings: "[^"]+"

        # Format of symboltable [ KEY, (NAME, CLASS, TYPE, SCOPE, VALUE, LINE DECLARED, LINE REFERENCED) ]

        # Clear previous lines from memory
        linecache.clearcache()

        # Retrieve current line from file
        self.line = linecache.getline(self.file, self.lineNumber + 1)

        # EOF
        if not self.line:
            self.listToken.append(Token('EOF', 'EOF'))
            return self.listToken

        # Strip tab keys since they're not a problem in this language
        # self.line = self.line.replace('\t', ' ')

        if plist:
            self.listToken = list
        else:
            self.listToken = []

        if strerr:
            auto = 'string_error'
            self.lineNumber -= 1
        else:
            auto = 'begin'
            
        string = ''
        isString = False
        tmpSizeListToken = 0

        state = 0
        tmp = ''

        for c in self.line:
            
            string += c
            
            # Comment automaton
            if auto == 'comment':
                if c != '}':
                    if c == '\n':
                        if not isString:
                            self.errorRef.lexerError('Linha ' + str(self.lineNumber + 2) + ': ' + 'comentario nao fechado')
                        auto = 'begin'
                elif c == '}':
                    auto = 'begin'
                    continue

            # Number automaton
            if auto == 'number':
                if state == 1:
                    if c.isdigit():
                        tmp += c
                        continue
                    else:
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

            # Symbols automaton
            if auto == 'symbol':
                    if tmp+c in self.symtable.table:
                        tmp += c
                    elif tmp in self.symtable.table:
                        self.listToken.append(Token(tmp, tmp))
                        auto = 'begin'
                    else:
                        if not isString:
                            self.errorRef.lexerError('Linha ' + str(self.lineNumber + 1) + ': ' + tmp + ' - simbolo nao identificado')
                        auto = 'begin'

            # Names automaton
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
                        if self.symtable.table[tmp]['token'] == 'identificador':
                            self.listToken.append(Token(tmp, 'identificador'))
                        else:
                            self.listToken.append(Token(tmp, tmp))
                    else:
                        #self.symtable.insertSymbol(tmp, (tmp, 'variavel', 'identificador', self.scope, 'null', self.lineNumber, self.lineNumber))
                        self.listToken.append(Token(tmp, 'identificador'))
                    auto = 'begin'

            # Checks which automaton to enter
            if auto == 'begin':
                tmp = ''
                state = 1
                if c == '\t' or c == '\n' or c == ' ' or c == '\r':
                        continue
                elif c == '"':
                    tmp += c
                    auto = 'string'
                elif c == '{':
                    auto = 'comment'
                elif c.isdigit():
                    tmp += c
                    auto = 'number'
                elif not c.isalnum() and c != "_":
                    tmp += c
                    auto = 'symbol'
                elif c.isalpha() or c == '_':
                    tmp += c
                    auto = 'names'
                    
            # String
            if auto == 'string':
                if not isString:
                    isString = True
                    tmpSizeListToken = len(self.listToken)
                    string = c
                    self.listToken.append(Token('Linha ' + str(self.lineNumber + 1) + ': ' + tmp, 'simbolo nao identificado', True))
                    self.listMessage.append('Linha ' + str(self.lineNumber + 1) + ': ' + tmp + ' - simbolo nao identificado')
                else:
                    tmpSizeListToken = len(self.listToken) - tmpSizeListToken
                    for i in range(tmpSizeListToken):
                        self.listToken.pop()

                    self.listMessage.pop()

                    self.listToken.append(Token(string, 'cadeia_literal'))
                    string = ''
                    isString = False
                auto = 'begin'

        #End of analysis, increment lineNumber
        self.lineNumber += 1

        # Check whether the error message list is empty or there is a message there indicating
        # that some string wasn't properly closed thus indicating that there's a error that must
        # be treated by the Error class.
        if self.listMessage:
            msg = str(self.listMessage.pop())
            self.errorRef.lexerError(msg)

        return self.listToken