__author__ = 'thiago'

from Classes.Token import Token


class CodeGenerator(object):
    # Constructor
    def __init__(self, ly, out):
        self.ly = ly
        self.out = out
        self.script = []

        self.listToken = []

        # This variable stores the current token being analysed
        self.currentToken = Token('', '')

    # Helper methods
    def getToken(self):
        # Obtain the first token on the list
        while not self.listToken:
            self.listToken = self.ly.getToken()

        self.currentToken = self.listToken.pop(0)

    # Generator Code Method
    def code(self):
        self.script.append('#include <stdio.h>')
        self.script.append('#include <stdlib.h>')
        self.getToken()

        #while(self.currentToken.category != 'fim_algoritmo'):
        if self.currentToken.category == 'algoritmo':
            self.script.append('int main()')
            self.script.append('{')
            self.getToken()

        if self.currentToken.category == 'declare':
            self.getToken()
            self.declare()
            self.getToken()


        # fim_algoritmo
        self.script.append('}')


        return self.script

    def declare(self):
        variaveis = []
        temp = ''

        if self.currentToken.category == 'identificador':
            variaveis.append(self.currentToken.name)
            self.getToken()

            while self.currentToken.category == ',':
                self.getToken()

                if self.currentToken.category == 'identificador':
                    variaveis.append(self.currentToken.name)
                    self.getToken()

            if self.currentToken.category == ':':
                self.getToken()

            if self.currentToken.category == 'inteiro':
                temp = 'int'
            elif self.currentToken.category == 'real':
                temp = 'double'
            elif self.currentToken.category == 'literal':
                temp = 'char'


            if temp == 'int' or temp == 'double':
                temp += ' ' + variaveis.pop(0)
                for v in variaveis:
                    temp += ', ' + v
                self.script.append(temp + ';')

            else:
                temp += ' ' + variaveis.pop(0)
                if not variaveis:
                    temp += '[50]'
                else:
                    for v in variaveis:
                        temp += ', ' + v + '[50]'
                self.script.append(temp + ';')