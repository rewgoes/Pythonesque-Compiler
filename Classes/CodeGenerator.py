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

        self.prealgoritmo()

        self.algoritmo()

        return self.script

    # pre Algoritmo
    def prealgoritmo(self):

        while self.currentToken.category == 'procedimento' or self.currentToken.category == 'funcao' or self.currentToken.category == 'constante':
            if self.currentToken.category == 'procedimento':
                pass
            elif self.currentToken.category == 'funcao':
                pass
            else:
                pass

    # algoritmo
    def algoritmo(self):
        if self.currentToken.category == 'algoritmo':
            self.script.append('int main()')
            self.script.append('{')
            self.getToken()

        self.comandos()

        # fim_algoritmo
        self.script.append('}')

    def declare(self):
        variaveis = []
        temp = ''

        if self.currentToken.category == 'declare':
            self.getToken()
            self.declare()
            self.getToken()

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

        else:
            pass

    def comandos(self):

        while self.currentToken.category == 'leia' or self.currentToken.category == 'escreva' or \
                self.currentToken.category == 'se' or self.currentToken.category == 'caso' or \
                self.currentToken.category == 'para' or self.currentToken.category == 'enquanto' or \
                self.currentToken.category == 'faca':

            if self.currentToken.category == 'leia':
                self.leia()
            elif self.currentToken.category == 'escreva':
                self.escreva()
            elif self.currentToken.category == 'se':
                self.se()
            elif self.currentToken.category == 'caso':
                self.caso()
            elif self.currentToken.category == 'para':
                self.para()
            elif self.currentToken.category == 'enquanto':
                self.enquanto()
            elif self.currentToken.category == 'faca':
                self.faca()

    def leia(self):
        pass

    def escreva(self):
        pass

    def se(self):
        pass

    def caso(self):
        pass

    def para(self):
        pass

    def enquanto(self):
        pass

    def faca(self):
        pass