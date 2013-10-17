__author__ = 'matheus'

#  from Classes.LexicalAy import LexicalAy


class Parser(object):

    def __init__(self):
        # Tokens read from input will populate this list
        # Parser will read this list until it's empty
        # When list is empty, parser will call LexicalAy.getToken()
        self.listToken = []

        # This variable stores the current token being analysed
        self.currentToken = 0

        # This is first-set of non-terminals ("primeiros")
        # It's a dictionary where the non-terminal/terminal is the key
        # And the value is a list with the firsts
        # Use the firstOf method to access the list
        # TODO: Complete the firstSet list, remember to check if the non-terminal you're doing is already in this list
        self.firstSet = \
            {'programa':  ['3', 'declare', 'constante', 'tipo', 'procedimento', 'funcao'],
             'declaracoes': ['3', 'declare', 'constante', 'tipo', 'procedimento', 'funcao' ],
             'declaracao_local_global': ['3', 'declare', 'constante', 'tipo', 'procedimento', 'funcao' ],
             'declaracao_global': ['declare', 'constante', 'tipo'],
             'declaracao_local': ['procedimento, funcao'],
             'variavel': ['^', '3'],
             'identificador': ['^', '3'],
             'ponteiro_opcional': ['^', '3'],
             'outros_ident': ['.'],
             'dimensao': ['['],
             'tipo': ['registro'],
             'registro': ['registro'],
             'mais_ident': [',', '3'],
             'mais_variaveis': ['^', '3'],
             'tipo_basico': ['literal', 'inteiro', 'real', 'logico'],
             'tipo_basico_ident': ['literal', 'inteiro', 'real', 'logico', 'IDENT'],  # How to handle this `IDENT` ?
             'tipo_estendido': ['^', '3']}

    # Helper methods

    def getToken(self):
        # Obtain the first token on the list
        if not self.listToken:
           # self.listToken = LexicalAy.getToken()
          pass

        self.currentToken = self.listToken.pop()

    def error(self):
        # TODO: Proper error handling
        pass

    def firstOf(self, term):
        if term in self.firstSet:
            # non-terminal
            return self.firstSet.get(term)
        else:
            # terminal
            return term

    # Grammar rules
    def programa(self):
        # <declaracoes> algoritmo <corpo> fim_algoritmo
            self.declaracoes()

            if self.currentToken == 'algoritmo':
                self.getToken()
            else:
                self.error()

            self.corpo()

            if self.currentToken == 'fim_algoritmo':
                self.getToken()
            else:
                self.error()

    def declaracoes(self):
        # <decl_local_global> <declaracoes> | 3
        while self.currentToken in self.firstOf('declaracoes'):  # [?]
            self.getToken()
            self.decl_local_global()
            self.declaracoes()

    def decl_local_global(self):
        # <declaracao_local> | <declaracao_global>
        if self.currentToken in self.firstOf('declaracao_local'):
            self.declaracao_local()
        elif self.currentToken in self.firstOf('declaracao_global'):
            self.declaracao_global()
        else:
            self.error()

    def declaracao_local(self):
        # declare <variavel>
        # | constante IDENT : <tipo_basico> = <valor_constante>
        # | tipo IDENT : <tipo>
        if self.currentToken == 'declare':
            self.getToken()
            self.variavel()
        elif self.currentToken == 'constante':
            # TODO: IDENT again, what to do with this?
            self.getToken()
            if self.currentToken == ':':
                self.getToken()
                self.tipo_basico()
                if self.currentToken == '=':
                    self.getToken()
                    self.valor_constante()
                else:
                    self.error()
            else:
                self.error()

        elif self.currentToken == 'tipo':
            # IDENT
            self.getToken()
            if self.currentToken == ':':
                self.getToken()
                self.tipo()
            else:
                self.error()
        else:
            self.error()

    def variavel(self):
        # <identificador> <mais_ident> : <tipo>
        pass

    def identificador(self):
        # <ponteiro_opcional> IDENT <outros_ident> <dimensao>
        pass

    def ponteiro_opcional(self):
        # ^ | 3
        pass

    def outros_ident(self):
        # . IDENT <outros_ident> | 3
        pass

    def dimensao(self):
        # [ <exp_aritmetica ] <dimensao> | 3
        pass

    def tipo(self):
        # <registro> | <tipo_estendido>
        pass

    def mais_ident(self):
        # , <identificador> <mais_ident> | 3
        pass

    def mais_variaveis(self):
        # <variavel> <mais_variaveis> | 3
        pass

    def tipo_basico(self):
        # literal | inteiro | real | logico
        pass

    def tipo_basico_ident(self):
        # <tipo_basico> | IDENT
        pass

    def tipo_estendido(self):
        # <ponteiro_opcional> <tipo_basico_ident>
        pass

    def corpo(self):
        # <declaracoes_locais> <comandos>
        pass

    def declaracao_global(self):
        # procedimento IDENT ( <parametros_opcional> ) <declaracoes_locais> <comandos> fim_procedimento
        # | funcao IDENT ( <parametros_opcional> ) : <tipo_estendido> <declaracoes_locais> <comandos> fim_funcao
        pass

    def tipo_basico(self):
        pass

    def valor_constante(self):
        pass

    # TODO: other methods, remove 'pass' if writing in one of these